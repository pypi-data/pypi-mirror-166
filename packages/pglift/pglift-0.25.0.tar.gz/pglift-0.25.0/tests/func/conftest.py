import logging
import pathlib
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
)
from unittest.mock import patch

import pgtoolkit.conf
import port_for
import psycopg.conninfo
import pydantic
import pytest
from pydantic.utils import deep_update

from pglift import _install, instances, pgbackrest, prometheus, temboard
from pglift._compat import Protocol
from pglift._install import (
    BACKUP_SERVICE_NAME,
    BACKUP_TIMER_NAME,
    POSTGRESQL_SERVICE_NAME,
)
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import (
    PgBackRestSettings,
    PostgreSQLSettings,
    PrometheusSettings,
    Settings,
    TemboardSettings,
)

from . import AuthType, execute


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--systemd",
        action="store_true",
        default=False,
        help="Run tests with systemd as service manager/scheduler",
    )


def pytest_report_header(config: Any) -> List[str]:
    systemd = config.option.systemd
    return [f"systemd: {systemd}"]


@pytest.fixture(autouse=True)
def journalctl(systemd_requested: bool) -> Iterator[None]:
    journalctl = shutil.which("journalctl")
    if not systemd_requested or journalctl is None:
        yield
        return
    proc = subprocess.Popen([journalctl, "--user", "-f", "-n0"])
    yield
    proc.kill()


@pytest.fixture(scope="package")
def systemd_available() -> bool:
    try:
        subprocess.run(
            ["systemctl", "--user", "status"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return True


@pytest.fixture(scope="package")
def powa_available(no_plugins: bool, pg_bindir: Tuple[pathlib.Path, str]) -> bool:
    if no_plugins:
        return False
    pg_config = pg_bindir[0] / "pg_config"
    result = subprocess.run(
        [pg_config, "--pkglibdir"],
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True,
    )
    pkglibdir = pathlib.Path(result.stdout.strip())
    return (
        (pkglibdir / "pg_qualstats.so").exists()
        and (pkglibdir / "pg_stat_kcache.so").exists()
        and (pkglibdir / "powa.so").exists()
    )


@pytest.fixture(scope="package")
def systemd_requested(request: Any, systemd_available: bool) -> bool:
    value = request.config.option.systemd
    assert isinstance(value, bool)
    if value and not systemd_available:
        raise pytest.UsageError("systemd is not available on this system")
    return value


@pytest.fixture(scope="package", params=list(AuthType), ids=lambda v: f"auth:{v}")
def postgresql_auth(request: Any) -> AuthType:
    assert isinstance(request.param, AuthType)
    return request.param


@pytest.fixture(scope="package")
def site_config(
    site_config: Callable[..., pathlib.Path], postgresql_auth: AuthType
) -> Iterator[Callable[..., pathlib.Path]]:
    if postgresql_auth == AuthType.peer:

        datadir = pathlib.Path(__file__).parent / "data" / "peer"
    else:
        datadir = pathlib.Path(__file__).parent / "data" / "base"

    def test_site_config(*parts: str) -> Optional[pathlib.Path]:
        """Lookup for configuration files in local data director first."""
        fpath = datadir.joinpath(*parts)
        if fpath.exists():
            return fpath
        return site_config(*parts)

    with patch("pglift.util.site_config", new=test_site_config) as fn:
        yield fn  # type: ignore[misc]


@pytest.fixture(scope="package")
def postgresql_settings(
    tmp_path_factory: pytest.TempPathFactory,
    postgresql_auth: AuthType,
    surole_password: str,
    pgbackrest_password: str,
) -> PostgreSQLSettings:
    passfile = tmp_path_factory.mktemp("home") / ".pgpass"
    if postgresql_auth == AuthType.pgpass:
        passfile.touch(mode=0o600)
    auth: Dict[str, Any] = {
        "local": "password",
        "passfile": str(passfile),
    }
    surole: Dict[str, Any] = {"name": "postgres"}
    backuprole: Dict[str, Any] = {"name": "backup"}
    if postgresql_auth == AuthType.peer:
        pass  # See also PeerAuthContext.
    elif postgresql_auth == AuthType.password_command:
        passcmdfile = tmp_path_factory.mktemp("home") / "passcmd"
        auth["password_command"] = [str(passcmdfile), "{instance}", "{role}"]
        with passcmdfile.open("w") as f:
            f.write(
                dedent(
                    f"""\
                    #!/bin/sh
                    instance=$1
                    role=$2
                    if [ ! "$instance" ]
                    then
                        echo "no instance given!!" >&2
                        exit 1
                    fi
                    if [ ! "$role" ]
                    then
                        echo "no role given!!" >&2
                        exit 1
                    fi
                    if [ "$role" = {surole["name"]} ]
                    then
                        echo "retrieving password for $role for $instance..." >&2
                        echo {surole_password}
                        exit 0
                    fi
                    if [ "$role" = {backuprole["name"]} ]
                    then
                        echo "retrieving password for $role for $instance..." >&2
                        echo {pgbackrest_password}
                        exit 0
                    fi
                    """
                )
            )
        passcmdfile.chmod(0o700)
    elif postgresql_auth == AuthType.pgpass:
        surole["pgpass"] = True
        backuprole["pgpass"] = True
    else:
        raise AssertionError(f"unexpected {postgresql_auth}")
    return PostgreSQLSettings.parse_obj(
        {
            "root": str(tmp_path_factory.mktemp("postgres")),
            "auth": auth,
            "surole": surole,
            "backuprole": backuprole,
        }
    )


@pytest.fixture(scope="package")
def settings(
    request: Any,
    postgresql_settings: PostgreSQLSettings,
    tmp_path_factory: pytest.TempPathFactory,
    systemd_requested: bool,
    systemd_available: bool,
    pgbackrest_available: bool,
    prometheus_execpath: Optional[pathlib.Path],
    powa_available: bool,
    temboard_execpath: Optional[pathlib.Path],
) -> Settings:
    prefix = tmp_path_factory.mktemp("prefix")
    (prefix / "run" / "postgresql").mkdir(parents=True)
    obj = {
        "prefix": str(prefix),
        "run_prefix": str(tmp_path_factory.mktemp("run")),
        "postgresql": postgresql_settings.dict(),
    }
    if systemd_requested:
        obj.update({"systemd": {}})

    if obj.get("service_manager") == "systemd" and not systemd_available:
        pytest.skip("systemd not functional")

    if pgbackrest_available:
        obj["pgbackrest"] = {}

    if prometheus_execpath:
        obj["prometheus"] = {"execpath": prometheus_execpath}

    if powa_available:
        obj["powa"] = {}

    if temboard_execpath:
        obj["temboard"] = {"execpath": temboard_execpath}

    try:
        s = Settings.parse_obj(obj)
    except pydantic.ValidationError as exc:
        pytest.skip(
            "; ".join(
                f"unsupported setting(s) {' '.join(map(str, e['loc']))}: {e['msg']}"
                for e in exc.errors()
            )
        )

    return s


@pytest.fixture(scope="package")
def ctx(settings: Settings) -> Context:
    return Context(settings=settings)


@pytest.fixture(autouse=True)
def _hook_logger(ctx: Context) -> None:
    hook_level = logging.DEBUG - 1
    logging.addLevelName(hook_level, "HOOK")
    logger = logging.getLogger(__name__)
    logger.setLevel(hook_level)

    def before(
        hook_name: str, hook_impls: Sequence[Any], kwargs: Dict[str, Any]
    ) -> None:
        def p(value: Any) -> str:
            s = str(value)
            if len(s) >= 20:
                s = f"{s[:17]}..."
            return s

        logger.log(
            hook_level,
            "calling hook %s(%s) with implementations: %s",
            hook_name,
            ", ".join(f"{k}={p(v)}" for k, v in kwargs.items()),
            ", ".join(i.plugin_name for i in hook_impls),
        )

    def after(
        outcome: Any, hook_name: str, hook_impls: Sequence[Any], kwargs: Dict[str, Any]
    ) -> None:
        logger.log(hook_level, "outcome of %s: %s", hook_name, outcome.get_result())

    ctx.pm.add_hookcall_monitoring(before, after)


@pytest.fixture(scope="package", autouse=True)
def _installed(
    ctx: Context,
    systemd_requested: bool,
    tmp_path_factory: pytest.TempPathFactory,
    override_systemd_unit_start_limit: Iterator[None],
) -> Iterator[None]:
    if not systemd_requested:
        yield
        return

    tmp_path = tmp_path_factory.mktemp("config")
    settings = ctx.settings
    assert settings.service_manager == "systemd"

    custom_settings = tmp_path / "settings.json"
    custom_settings.write_text(settings.json())
    assert _install.do(
        ctx,
        env=f"SETTINGS=@{custom_settings}",
        header=f"# ** Test run on {platform.node()} at {datetime.now().isoformat()} **",
    )
    yield
    assert _install.undo(ctx)


@pytest.fixture(scope="package")
def override_systemd_unit_start_limit(
    ctx: Context, systemd_requested: bool
) -> Iterator[None]:
    """Override the systemd configuration for the instance to prevent
    errors when too many starts happen in a short amount of time
    """
    if not systemd_requested:
        yield
        return
    units = [
        POSTGRESQL_SERVICE_NAME,
        BACKUP_SERVICE_NAME,
        BACKUP_TIMER_NAME,
    ]
    overrides_dir = Path("~/.config/systemd/user").expanduser()
    overrides = [overrides_dir / f"{unit}.d" / "override.conf" for unit in units]
    for override in overrides:
        override.parent.mkdir(parents=True, exist_ok=True)
        content = """
        [Unit]
        StartLimitIntervalSec=0
        """
        override.write_text(dedent(content))

    yield

    for override in overrides:
        ctx.rmtree(override.parent)


@pytest.fixture
def pgbackrest_settings(ctx: Context) -> PgBackRestSettings:
    settings = pgbackrest.available(ctx.settings)
    if settings is None:
        pytest.skip("pgbackrest not available")
    return settings


@pytest.fixture
def prometheus_settings(ctx: Context) -> PrometheusSettings:
    settings = prometheus.available(ctx.settings)
    if settings is None:
        pytest.skip("prometheus not available")
    return settings


@pytest.fixture
def temboard_settings(ctx: Context) -> TemboardSettings:
    settings = temboard.available(ctx.settings)
    if settings is None:
        pytest.skip("temboard not available")
    return settings


@pytest.fixture(scope="package")
def tmp_port_factory() -> Iterator[int]:
    """Return a generator producing available and distinct TCP ports."""

    def available_ports() -> Iterator[int]:
        used: Set[int] = set()
        while True:
            port = port_for.select_random(exclude_ports=list(used))
            used.add(port)
            yield port

    return available_ports()


@pytest.fixture(scope="package")
def surole_password() -> str:
    return "s3kret p@Ssw0rd!"


@pytest.fixture(scope="package")
def replrole_password(settings: Settings) -> str:
    return "r3pl p@Ssw0rd!"


@pytest.fixture(scope="package")
def prometheus_password() -> str:
    # TODO: use a password with blanks when
    # https://github.com/prometheus-community/postgres_exporter/issues/393 is fixed
    return "prom3th3us-p@Ssw0rd!"


@pytest.fixture(scope="package")
def temboard_password() -> str:
    return "tembo@rd p@Ssw0rd!"


@pytest.fixture(scope="package")
def powa_password() -> str:
    return "P0w4 p@Ssw0rd!"


@pytest.fixture(scope="package")
def pgbackrest_password() -> str:
    return "b4ckup p@Ssw0rd!"


@pytest.fixture(scope="package")
def composite_instance_model(ctx: Context) -> Type[interface.Instance]:
    return interface.Instance.composite(ctx.pm)


@pytest.fixture(scope="package")
def log_directory(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("postgres-logs")


T_co = TypeVar("T_co", covariant=True)


class Factory(Protocol[T_co]):
    def __call__(self, name: str, state: str = ..., **kwargs: Any) -> T_co:
        ...


@pytest.fixture(scope="package")
def instance_manifest_factory(
    settings: Settings,
    ctx: Context,
    pg_version: str,
    surole_password: str,
    replrole_password: str,
    pgbackrest_password: str,
    prometheus_password: str,
    temboard_password: str,
    powa_password: str,
    log_directory: pathlib.Path,
    tmp_port_factory: Iterator[int],
    composite_instance_model: Type[interface.Instance],
) -> Factory[interface.Instance]:
    def factory(name: str, state: str = "stopped", **kwargs: Any) -> interface.Instance:
        port = next(tmp_port_factory)
        services = {}
        if settings.prometheus:
            services["prometheus"] = {
                "port": next(tmp_port_factory),
                "password": prometheus_password,
            }
        if settings.powa:
            services["powa"] = {"password": powa_password}
        if settings.temboard:
            services["temboard"] = {
                "password": temboard_password,
                "port": next(tmp_port_factory),
            }
        if settings.pgbackrest:
            services["pgbackrest"] = {"password": pgbackrest_password}
        m = {
            "name": name,
            "version": pg_version,
            "state": state,
            "port": port,
            "auth": {
                "host": "reject",
            },
            "configuration": {
                "log_directory": str(log_directory),
                # Keep logs to stderr in tests so that they are captured by pytest.
                "logging_collector": False,
            },
            "surole_password": surole_password,
            "replrole_password": replrole_password,
            "extensions": ["passwordcheck"],
            **services,
        }
        m = deep_update(m, kwargs)
        return composite_instance_model.parse_obj(m)

    return factory


@pytest.fixture(scope="package")
def instance_manifest(
    instance_manifest_factory: Factory[interface.Instance],
) -> interface.Instance:
    return instance_manifest_factory("test")


@pytest.fixture
def instance_factory(
    ctx: Context, instance_manifest_factory: Factory[interface.Instance]
) -> Iterator[Factory[Tuple[interface.Instance, system.Instance]]]:
    values: Dict[str, system.Instance] = {}

    def factory(
        name: str, state: str = "stopped", **kwargs: Any
    ) -> Tuple[interface.Instance, system.Instance]:
        assert name not in values, f"{name} already used"
        m = instance_manifest_factory(name, state=state, **kwargs)
        result = instances.apply(ctx, m)
        assert result.change_state == interface.ApplyChangeState.created
        i = system.Instance.system_lookup(ctx, (m.name, m.version))
        values[name] = i
        return m, i

    yield factory

    for i in values.values():
        if instances.exists(ctx, i.name, i.version):
            instances.drop(ctx, i)


@pytest.fixture(scope="package")
def instance(
    ctx: Context, instance_manifest: interface.Instance
) -> Iterator[system.Instance]:
    assert instances.apply(ctx, instance_manifest)
    instance = system.Instance.system_lookup(
        ctx, (instance_manifest.name, instance_manifest.version)
    )
    # Limit postgresql.conf to uncommented entries to reduce pytest's output
    # due to --show-locals.
    postgresql_conf = instance.datadir / "postgresql.conf"
    postgresql_conf.write_text(
        "\n".join(
            line
            for line in postgresql_conf.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    )
    yield instance
    if instances.exists(ctx, instance.name, instance.version):
        instances.drop(ctx, instance)


@pytest.fixture(scope="package")
def standby_manifest(
    settings: Settings,
    instance: system.Instance,
    replrole_password: str,
    instance_manifest_factory: Factory[interface.Instance],
) -> interface.Instance:
    primary_conninfo = psycopg.conninfo.make_conninfo(
        host=settings.postgresql.socket_directory,
        port=instance.port,
        user=settings.postgresql.replrole,
    )
    return instance_manifest_factory(
        "standby",
        standby={
            "for": primary_conninfo,
            "password": replrole_password,
            "slot": "standby",
        },
    )


@pytest.fixture(scope="package")
def standby_instance(
    ctx: Context,
    postgresql_auth: AuthType,
    standby_manifest: interface.Instance,
    instance: system.Instance,
) -> Iterator[system.Instance]:
    with instances.postgresql_running(ctx, instance):
        standby = standby_manifest._standby()
        assert standby is not None
        execute(
            ctx,
            instance,
            f"SELECT true FROM pg_create_physical_replication_slot('{standby.slot}')",
            fetch=False,
        )
        instances.apply(ctx, standby_manifest)
    stdby_instance = system.Instance.system_lookup(
        ctx, (standby_manifest.name, standby_manifest.version)
    )
    instances.stop(ctx, stdby_instance)
    yield stdby_instance
    if instances.exists(ctx, stdby_instance.name, stdby_instance.version):
        instances.drop(ctx, stdby_instance)


@pytest.fixture(scope="package")
def upgraded_instance(
    ctx: Context,
    instance: system.Instance,
    tmp_port_factory: Iterator[int],
    composite_instance_model: Type[interface.Instance],
) -> Iterator[system.Instance]:
    upgraded = instances.upgrade(
        ctx,
        instance,
        name="upgraded",
        version=instance.version,
        port=next(tmp_port_factory),
        _instance_model=composite_instance_model,
    )
    yield upgraded
    if instances.exists(ctx, upgraded.name, upgraded.version):
        instances.drop(ctx, upgraded)


def _drop_instance(
    ctx: Context, instance: system.Instance
) -> pgtoolkit.conf.Configuration:
    config = instance.config()
    if instances.exists(ctx, instance.name, instance.version):
        instances.drop(ctx, instance)
    return config


@pytest.fixture(scope="package")
def instance_dropped(
    ctx: Context, instance: system.Instance
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(ctx, instance)


@pytest.fixture(scope="package")
def standby_instance_dropped(
    ctx: Context, standby_instance: system.Instance
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(ctx, standby_instance)


@pytest.fixture(scope="package")
def upgraded_instance_dropped(
    ctx: Context, upgraded_instance: system.Instance
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(ctx, upgraded_instance)


class RoleFactory(Protocol):
    def __call__(self, name: str, options: str = "") -> None:
        ...


@pytest.fixture()
def role_factory(ctx: Context, instance: system.Instance) -> Iterator[RoleFactory]:
    rolnames = set()

    def factory(name: str, options: str = "") -> None:
        if name in rolnames:
            raise ValueError(f"'{name}' name already taken")
        execute(ctx, instance, f"CREATE ROLE {name} {options}", fetch=False)
        rolnames.add(name)

    yield factory

    for name in rolnames:
        execute(ctx, instance, f"DROP ROLE IF EXISTS {name}", fetch=False)


class DatabaseFactory(Protocol):
    def __call__(self, name: str) -> None:
        ...


@pytest.fixture()
def database_factory(
    ctx: Context, instance: system.Instance
) -> Iterator[DatabaseFactory]:
    datnames = set()

    def factory(name: str, *, owner: Optional[str] = None) -> None:
        if name in datnames:
            raise ValueError(f"'{name}' name already taken")
        sql = f"CREATE DATABASE {name}"
        if owner:
            sql += f" OWNER {owner}"
        execute(ctx, instance, sql, fetch=False)
        datnames.add(name)

    yield factory

    for name in datnames:
        execute(
            ctx,
            instance,
            f"DROP DATABASE IF EXISTS {name}",
            fetch=False,
        )
