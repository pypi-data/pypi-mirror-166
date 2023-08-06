from pathlib import Path
from typing import Type
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pglift import exceptions, instances
from pglift.cli import CLIContext, Obj
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.patroni import (
    configure_postgresql,
    impl,
    install_systemd_unit_template,
    instance_env,
    models,
    uninstall_systemd_unit_template,
)
from pglift.patroni.cli import cli as cli
from pglift.settings import PatroniSettings, Settings, SystemdSettings

from . import click_result_traceback


@pytest.fixture
def patroni_bin_dir(tmp_path: Path) -> Path:
    bindir = tmp_path
    for name in ("patroni", "patronictl"):
        execpath = bindir / name
        execpath.touch(0o700)
        execpath.write_text("#!/bin/sh\nexit 1\n")
    return bindir


@pytest.fixture
def settings(settings: Settings, patroni_bin_dir: Path) -> Settings:
    s = settings.dict()
    s["patroni"] = {"bin_dir": patroni_bin_dir}
    with patch("shutil.which", return_value=True) as which:
        settings = Settings.parse_obj(s)
    which.assert_called_once_with("systemctl")
    return settings


@pytest.fixture
def patroni_settings(settings: Settings) -> PatroniSettings:
    assert settings.patroni
    return settings.patroni


@pytest.fixture
def instance_manifest(
    composite_instance_model: Type[interface.Instance],
) -> interface.Instance:
    return composite_instance_model.parse_obj(
        {
            "name": "test",
            "version": "11",
            "data_checksums": True,
            "configuration": {
                "shared_buffers": "257MB",
                "effective_cache_size": "4 GB",
                "unix_socket_directories": "/tmp/tests",
            },
            "surole_password": None,
            "replrole_password": "rrr",
            "extensions": ["passwordcheck"],
            "patroni": {"cluster": "whatever"},
        }
    )


@pytest.fixture
def instance(
    datadir: Path, patroni_settings: PatroniSettings, instance: system.Instance
) -> system.Instance:
    patroni_config = impl._configpath(instance.qualname, patroni_settings)
    patroni_config.parent.mkdir(parents=True, exist_ok=True)
    patroni_config.write_text((datadir / "patroni.yaml").read_text())
    patroni = models.Service(cluster="test-scope", node="pg1")
    instance.services.append(patroni)
    return instance


def test_available(settings: Settings) -> None:
    assert impl.available(settings)


def test_install_systemd_unit_template(
    ctx: Context, systemd_settings: SystemdSettings, patroni_bin_dir: Path
) -> None:
    install_systemd_unit_template(ctx, systemd_settings)
    unit = systemd_settings.unit_path / "pglift-patroni@.service"
    assert unit.exists()
    lines = unit.read_text().splitlines()
    assert (
        f"ExecStart={patroni_bin_dir / 'patroni'} {ctx.settings.prefix}/etc/patroni/%i.yaml"
        in lines
    )
    uninstall_systemd_unit_template(ctx, systemd_settings)
    assert not unit.exists()


@pytest.fixture
def patroni(
    ctx: Context,
    settings: Settings,
    instance: system.Instance,
    instance_manifest: interface.Instance,
) -> models.Patroni:
    m = instance_manifest._copy_validate(
        {
            "version": "11",
            "data_checksums": True,
            "configuration": {
                "shared_buffers": "257MB",
                "effective_cache_size": "4 GB",
                "unix_socket_directories": "/tmp/tests",
            },
            "surole_password": None,
            "replrole_password": "rrr",
        }
    )
    with patch(
        "pglift.pgbackrest.impl._configpath", return_value="/cfg/pgbackrest/my.conf"
    ) as configpath, patch(
        "socket.gethostbyname",
        side_effect=AssertionError("gethostbyname unexpectedly called"),
    ):
        p = models.Patroni.build(
            "test-scope",
            "pg1",
            "pghost.test",
            ctx,
            instance,
            m,
            restapi={"connect_address": "localhost:8080"},
            zookeeper={"hosts": ["server:123"]},
        )
    configpath.assert_called_once_with(f"11-{instance.name}", settings.pgbackrest)
    return p


def test_yaml(patroni: models.Patroni, datadir: Path, write_changes: bool) -> None:
    patroni = patroni.copy(
        update={
            "postgresql": patroni.postgresql.copy(
                update={
                    "bin_dir": ".",
                    "data_dir": Path("test-datadir"),
                }
            ),
        }
    )
    doc = patroni.yaml()
    fpath = datadir / "patroni.yaml"
    if write_changes:
        fpath.write_text(doc)
    expected = fpath.read_text()
    assert doc == expected


def test_postgresql_conf(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_conf(instance=instance).name == "postgresql.base.conf"


def test_postgresql_editable_conf(ctx: Context, instance: system.Instance) -> None:
    assert (
        ctx.hook.postgresql_editable_conf(ctx=ctx, instance=instance)
        == "\n".join(
            [
                "archive_command = '/usr/bin/pgbackrest --config=/cfg/pgbackrest/my.conf --stanza=11-test archive-push %p'",
                "archive_mode = on",
                "cluster_name = 'test'",
                "effective_cache_size = '4 GB'",
                "lc_messages = 'C'",
                "lc_monetary = 'C'",
                "lc_numeric = 'C'",
                "lc_time = 'C'",
                "log_destination = 'stderr'",
                "logging_collector = on",
                "port = 5432",
                "shared_buffers = '257MB'",
                "shared_preload_libraries = 'passwordcheck, pg_qualstats, pg_stat_statements, pg_stat_kcache'",
                "unix_socket_directories = '/tmp/tests'",
                "wal_level = 'replica'",
            ]
        )
        + "\n"
    )


def test_configure_postgresql(
    ctx: Context,
    patroni_settings: PatroniSettings,
    instance_manifest: interface.Instance,
    instance: system.Instance,
) -> None:
    instance_manifest.configuration["work_mem"] = "8MB"
    pgconfig = instances.configuration(ctx, instance_manifest, instance)
    patroni = impl.config(instance.qualname, patroni_settings)
    postgresql_parameters = patroni.postgresql.parameters.copy()
    assert "work_mem" not in postgresql_parameters
    postgresql_parameters["work_mem"] = "8MB"
    with patch.object(impl, "api_request") as api_request:
        changes = configure_postgresql(ctx, instance_manifest, pgconfig, instance)
    old, new = changes.pop("archive_command")
    assert changes == {"work_mem": (None, "8MB")}
    assert postgresql_parameters["archive_command"] == old
    postgresql_parameters["archive_command"] = new
    (p, verb, endpoint), _ = api_request.call_args
    assert (verb, endpoint) == ("POST", "reload")
    assert p.postgresql.parameters == postgresql_parameters


def test_env(ctx: Context, instance: system.Instance, pg_version: str) -> None:
    assert instance_env(ctx, instance) == {
        "PATRONICTL_CONFIG_FILE": f"{ctx.settings.prefix}/etc/patroni/{pg_version}-test.yaml",
        "PATRONI_NAME": "pg1",
        "PATRONI_SCOPE": "test-scope",
    }


def test_api_request(patroni: models.Patroni) -> None:
    with patch("requests.request") as request:
        impl.api_request(patroni, "GET", "readiness")
    request.assert_called_once_with("GET", "http://localhost:8080/readiness")


def test_check_api_status(settings: Settings, instance: system.Instance) -> None:
    assert settings.patroni
    assert not impl.check_api_status(instance.qualname, settings.patroni)


def test_promote_postgresql(ctx: Context, instance: system.Instance) -> None:
    assert ctx.settings.patroni
    with pytest.raises(exceptions.UnsupportedError):
        ctx.hook.promote_postgresql(ctx=ctx, instance=instance)


def test_cli_patroni_logs(settings: Settings, instance: system.Instance) -> None:
    runner = CliRunner()
    ctx = CLIContext(settings=settings)
    obj = Obj(context=ctx)
    with patch.object(impl, "logs", return_value=["l1\n", "l2\n"]) as logs:
        result = runner.invoke(cli, ["-i", str(instance), "logs"], obj=obj)
    assert result.exit_code == 0, click_result_traceback(result)
    logs.assert_called_once_with(instance.qualname, ctx.settings.patroni)
    assert result.output == "l1\nl2\n"
