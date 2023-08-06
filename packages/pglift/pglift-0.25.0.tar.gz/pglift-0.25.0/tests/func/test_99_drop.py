import pathlib

import pytest
import requests
from pgtoolkit.conf import Configuration

from pglift import exceptions, systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import PgBackRestSettings, PrometheusSettings
from pglift.systemd import scheduler, service_manager

from . import AuthType


def test_pgpass(
    ctx: Context,
    postgresql_auth: AuthType,
    instance_manifest: interface.Instance,
    standby_instance_dropped: Configuration,
    upgraded_instance_dropped: Configuration,
    instance_dropped: Configuration,
) -> None:
    if postgresql_auth != AuthType.pgpass:
        pytest.skip("not applicable")
    passfile = ctx.settings.postgresql.auth.passfile
    assert not passfile.exists()


def test_systemd_backup_job(
    ctx: Context,
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    if ctx.settings.scheduler != "systemd":
        pytest.skip(f"not applicable for scheduler method '{ctx.settings.scheduler}'")

    unit = scheduler.unit("backup", instance.qualname)
    assert not systemd.is_active(ctx, unit)
    assert not systemd.is_enabled(ctx, unit)


def test_pgbackrest_teardown(
    ctx: Context,
    pgbackrest_settings: PgBackRestSettings,
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    configpath = pathlib.Path(
        str(pgbackrest_settings.configpath).format(name=instance.qualname)
    )
    directory = pathlib.Path(
        str(pgbackrest_settings.directory).format(name=instance.qualname)
    )
    lockpath = pathlib.Path(
        str(pgbackrest_settings.lockpath).format(name=instance.qualname)
    )
    spoolpath = pathlib.Path(
        str(pgbackrest_settings.spoolpath).format(name=instance.qualname)
    )
    assert not configpath.exists()
    assert not directory.exists()
    assert not lockpath.exists()
    assert not spoolpath.exists()


def test_prometheus_teardown(
    ctx: Context,
    prometheus_settings: PrometheusSettings,
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    configpath = pathlib.Path(
        str(prometheus_settings.configpath).format(name=instance.qualname)
    )
    queriespath = pathlib.Path(
        str(prometheus_settings.queriespath).format(name=instance.qualname)
    )
    assert not configpath.exists()
    assert not queriespath.exists()
    if ctx.settings.service_manager == "systemd":
        assert not systemd.is_enabled(
            ctx, service_manager.unit("postgres_exporter", instance.qualname)
        )
        with pytest.raises(requests.ConnectionError):
            requests.get("http://0.0.0.0:9187/metrics")


def test_databases_teardown(
    ctx: Context,
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    dumps_directory = pathlib.Path(
        str(ctx.settings.postgresql.dumps_directory).format(instance=instance)
    )
    assert not dumps_directory.exists()


def test_instance(
    ctx: Context, instance: system.Instance, instance_dropped: Configuration
) -> None:
    with pytest.raises(exceptions.InstanceNotFound, match=str(instance)):
        instance.exists()
