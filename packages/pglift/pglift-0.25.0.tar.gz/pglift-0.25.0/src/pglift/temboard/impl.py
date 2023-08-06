import configparser
import json
import logging
import socket
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pgtoolkit import conf as pgconf

from .. import cmd, exceptions, util
from ..models import interface, system
from ..task import task
from .models import ServiceManifest

if TYPE_CHECKING:
    from ..ctx import BaseContext
    from ..settings import Settings, TemboardSettings

service_name = "temboard_agent"


logger = logging.getLogger(__name__)


def available(settings: "Settings") -> Optional["TemboardSettings"]:
    return settings.temboard


def enabled(qualname: str, settings: "TemboardSettings") -> bool:
    return _configpath(qualname, settings).exists()


def _configpath(qualname: str, settings: "TemboardSettings") -> Path:
    return Path(str(settings.configpath).format(name=qualname))


def _userspath(qualname: str, settings: "TemboardSettings") -> Path:
    return Path(str(settings.users_path).format(name=qualname))


def _homedir(qualname: str, settings: "TemboardSettings") -> Path:
    return Path(str(settings.home).format(name=qualname))


def _pidfile(qualname: str, settings: "TemboardSettings") -> Path:
    return Path(str(settings.pid_file).format(name=qualname))


def _ssl_cert_file(qualname: str, settings: "TemboardSettings") -> Path:
    return settings.ssl_cert_dir / f"temboard-agent-{qualname}-selfsigned.pem"


def _ssl_key_file(qualname: str, settings: "TemboardSettings") -> Path:
    return settings.ssl_cert_dir / f"temboard-agent-{qualname}-selfsigned.key"


def config_var(configpath: Path, *, name: str, section: str) -> str:
    """Return temboardagent configuration value for given 'name' in 'section'."""
    if not configpath.exists():
        raise exceptions.FileNotFoundError(
            f"temboard agent configuration file {configpath} not found"
        )
    cp = configparser.ConfigParser()
    cp.read(configpath)
    for s, items in cp.items():
        if s != section:
            continue
        try:
            return items[name]
        except KeyError:
            pass
    raise exceptions.ConfigurationError(
        configpath, f"{name} not found in {section} section"
    )


def port(qualname: str, settings: "TemboardSettings") -> int:
    configpath = _configpath(qualname, settings)
    return int(config_var(configpath, name="port", section="temboard"))


def password(qualname: str, settings: "TemboardSettings") -> Optional[str]:
    configpath = _configpath(qualname, settings)
    try:
        return config_var(configpath, name="password", section="postgresql")
    except exceptions.ConfigurationError:
        return None


def secret_key(qualname: str, settings: "TemboardSettings") -> int:
    configpath = _configpath(qualname, settings)
    return int(config_var(configpath, name="key", section="temboard"))


@task("setting up temboardAgent")
def setup(
    ctx: "BaseContext",
    manifest: "interface.Instance",
    settings: "TemboardSettings",
    instance_config: pgconf.Configuration,
) -> None:
    """Setup temboardAgent"""
    service_manifest = manifest.service_manifest(ServiceManifest)
    if service_manifest is None:
        return

    instance = system.PostgreSQLInstance.system_lookup(
        ctx, (manifest.name, manifest.version)
    )

    configpath = _configpath(instance.qualname, settings)

    password_: Optional[str] = None
    if not configpath.exists():
        if service_manifest.password:
            password_ = service_manifest.password.get_secret_value()
    else:
        # Get the password from config file
        password_ = password(instance.qualname, settings)

    ssl_cert_file = _ssl_cert_file(instance.qualname, settings)
    ssl_key_file = _ssl_key_file(instance.qualname, settings)
    cert_name = ssl_cert_file.name
    key_name = ssl_key_file.name

    cp = configparser.ConfigParser()
    cp["temboard"] = {
        "port": str(service_manifest.port),
        "users": str(_userspath(instance.qualname, settings)),
        "plugins": json.dumps(settings.plugins),
        "ssl_cert_file": str(ssl_cert_file),
        "ssl_key_file": str(ssl_key_file),
        "key": util.generate_password(31, letters=False),
        "home": str(_homedir(instance.qualname, settings)),
    }

    # no longer needed when temboard ticket is done
    # https://github.com/dalibo/temboard/issues/1067
    hostname = socket.getfqdn()
    if "." not in hostname:
        cp["temboard"]["hostname"] = f"{hostname}.local"
    #

    cp["postgresql"] = {
        "user": settings.role,
        "instance": instance.qualname,
    }
    if "port" in instance_config:
        cp["postgresql"]["port"] = str(instance_config["port"])
    if "unix_socket_directories" in instance_config:
        pghost = instance_config.unix_socket_directories.split(",")[0]  # type: ignore[union-attr]
        cp["postgresql"]["host"] = pghost
    if password_:
        cp["postgresql"]["password"] = password_
    cp["logging"] = {
        "method": "stderr",
    }

    userspath = _userspath(instance.qualname, settings)
    userspath.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    userspath.touch(mode=0o600)

    homedir = _homedir(instance.qualname, settings)
    homedir.mkdir(mode=0o700, exist_ok=True, parents=True)

    pidfile = _pidfile(instance.qualname, settings)
    pidfile.parent.mkdir(mode=0o700, exist_ok=True, parents=True)

    configpath.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    cp_actual = configparser.ConfigParser()
    if configpath.exists():
        cp_actual.read(configpath)
    if cp != cp_actual:
        with configpath.open("w") as configfile:
            cp.write(configfile)
    ssl_cert_file.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    if not ssl_cert_file.exists() or not ssl_key_file.exists():
        crt, key = util.generate_certificate(run_command=ctx.run)
        ssl_dir = ssl_cert_file.parent
        for fname, content, mode in [(cert_name, crt, None), (key_name, key, 0o600)]:
            fpath = ssl_dir / fname
            if mode:
                fpath.touch(mode)
            fpath.write_text(content)

    ctx.hook.enable_service(ctx=ctx, service=service_name, name=instance.name)


@setup.revert("deconfiguring temboard agent")
def revert_setup(
    ctx: "BaseContext",
    manifest: "interface.Instance",
    settings: "TemboardSettings",
    instance_config: pgconf.Configuration,
) -> None:
    """Un-setup temboard"""
    instance = system.PostgreSQLInstance.system_lookup(
        ctx, (manifest.name, manifest.version)
    )

    configpath = _configpath(instance.qualname, settings)
    if configpath.exists():
        configpath.unlink()
    userspath = _userspath(instance.qualname, settings)
    if userspath.exists():
        userspath.unlink()
    pidfile = _pidfile(instance.qualname, settings)
    if pidfile.exists():
        pidfile.unlink()
    homedir = _homedir(instance.qualname, settings)
    if homedir.exists():
        ctx.rmtree(homedir)
    ssl_cert_file = _ssl_cert_file(instance.qualname, settings)
    if ssl_cert_file.exists():
        ssl_cert_file.unlink()
    ssl_key_file = _ssl_key_file(instance.qualname, settings)
    if ssl_key_file.exists():
        ssl_key_file.unlink()
    ctx.hook.disable_service(
        ctx=ctx, service=service_name, name=instance.name, now=True
    )


@task("starting temboard-agent service")
def start(
    ctx: "BaseContext",
    name: str,
    settings: "TemboardSettings",
    *,
    foreground: bool = False,
) -> None:
    """Start temboard-agent for `instance`"""
    if not enabled(name, settings):
        raise exceptions.InstanceNotFound(name)
    started = False
    if not foreground:
        started = ctx.hook.start_service(ctx=ctx, service=service_name, name=name)
    if not started:
        configpath = _configpath(name, settings)
        pidfile = _pidfile(name, settings)
        args = [
            str(settings.execpath),
            "--config",
            str(configpath),
        ]
        if foreground:
            cmd.execute_program(args, logger=logger)
        else:
            if cmd.status_program(pidfile) == cmd.Status.running:
                logger.debug("temboard-agent '%s' is already running", name)
                return
            cmd.Program(args, pidfile, logger=logger)


@task("stopping temboard-agent service")
def stop(
    ctx: "BaseContext",
    name: str,
    settings: "TemboardSettings",
) -> None:
    """Stop temboard-agent service"""
    if not enabled(name, settings):
        raise exceptions.InstanceNotFound(name)
    stopped = ctx.hook.stop_service(ctx=ctx, service=service_name, name=name)
    if not stopped:
        pidfile = _pidfile(name, settings)
        if cmd.status_program(pidfile) == cmd.Status.not_running:
            logger.info("temboard-agent '%s' is already stopped", name)
            return
        cmd.terminate_program(pidfile, logger=logger)
