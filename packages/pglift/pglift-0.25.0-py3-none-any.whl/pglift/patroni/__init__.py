import logging
from pathlib import Path
from typing import TYPE_CHECKING, Dict, NoReturn, Optional, Type

import pgtoolkit.conf

from .. import exceptions, hookimpl, systemd, util
from .._compat import Literal
from ..models import interface, system
from . import impl, models
from .impl import available as available

if TYPE_CHECKING:
    import click

    from ..ctx import BaseContext
    from ..settings import Settings, SystemdSettings
    from ..types import ConfigChanges

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


def service(instance: "system.Instance") -> models.Service:
    # Instances must have a "patroni" service, as long as the plugin is
    # enabled in settings.
    try:
        return instance.service(models.Service)
    except ValueError:
        raise exceptions.InstanceStateError(
            f"Patroni service not found on instance '{instance}'"
        )


@hookimpl  # type: ignore[misc]
def system_lookup(
    ctx: "BaseContext", instance: system.BaseInstance
) -> Optional[models.Service]:
    settings = available(ctx.settings)
    assert settings is not None
    patroni = impl.config(instance.qualname, settings)
    return models.Service(cluster=patroni.scope, node=patroni.name)


@hookimpl  # type: ignore[misc]
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl  # type: ignore[misc]
def standby_model() -> NoReturn:
    raise ValueError("standby not supported with Patroni")


@hookimpl  # type: ignore[misc]
def get(
    ctx: "BaseContext", instance: system.Instance
) -> Optional[models.ServiceManifest]:
    settings = available(ctx.settings)
    assert settings is not None
    s = service(instance)
    config = impl.config(instance.qualname, settings)
    cluster_members = impl.cluster_members(instance.qualname, settings)
    return models.ServiceManifest(
        cluster=s.cluster,
        node=s.node,
        postgresql_connect_host=config.postgresql.connect_address.host,
        etcd=config.etcd if settings.etcd_v2 else config.etcd3,
        restapi=config.restapi,
        cluster_members=cluster_members,
    )


SYSTEMD_SERVICE_NAME = "pglift-patroni@.service"


@hookimpl  # type: ignore[misc]
def install_systemd_unit_template(
    ctx: "BaseContext", systemd_settings: "SystemdSettings", header: str = ""
) -> None:
    logger.info("installing systemd template unit for Patroni")
    settings = available(ctx.settings)
    assert settings is not None
    configpath = str(settings.configpath).replace("{name}", "%i")
    content = systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(ctx.settings),
        configpath=configpath,
        bindir=settings.bin_dir,
    )
    systemd.install(
        SYSTEMD_SERVICE_NAME,
        util.with_header(content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@hookimpl  # type: ignore[misc]
def uninstall_systemd_unit_template(
    ctx: "BaseContext", systemd_settings: "SystemdSettings"
) -> None:
    logger.info("uninstalling systemd template unit for Patroni")
    systemd.uninstall(SYSTEMD_SERVICE_NAME, systemd_settings.unit_path, logger=logger)


@hookimpl  # type: ignore[misc]
def initdb(
    ctx: "BaseContext", manifest: interface.Instance, instance: system.BaseInstance
) -> Optional[Literal[True]]:
    """Initialize PostgreSQL database cluster through Patroni by configuring
    Patroni, then starting it (as the only way to get the actual instance
    created) and finally stopping it in order to respect initdb() hook
    contract and let further start logic apply.
    """
    settings = available(ctx.settings)
    assert settings is not None
    service = manifest.service_manifest(models.ServiceManifest)
    assert service is not None
    with impl.setup(
        ctx, instance, manifest, service, settings, validate=True, setup_logging=False
    ) as patroni:
        pass
    impl.init(ctx, instance, patroni, settings)
    impl.stop(ctx, instance.qualname, settings)
    return True


@hookimpl  # type: ignore[misc]
def configure_postgresql(
    ctx: "BaseContext",
    manifest: interface.Instance,
    configuration: pgtoolkit.conf.Configuration,
    instance: system.BaseInstance,
) -> Optional["ConfigChanges"]:
    """Build and validate Patroni configuration, and return changes to PostgreSQL configuration."""
    settings = available(ctx.settings)
    assert settings is not None
    service = manifest.service_manifest(models.ServiceManifest)
    assert service is not None
    with impl.setup(
        ctx, instance, manifest, service, settings, pgconfig=configuration
    ) as patroni:
        changes = impl.postgresql_changes(instance.qualname, patroni, settings)
    if changes:
        impl.reload(ctx, instance, settings)
    return changes


@hookimpl  # type: ignore[misc]
def configure_auth() -> Literal[True]:
    # No-op, since pg_hba.conf and pg_ident.conf are installed through Patroni
    # configuration.
    return True


@hookimpl  # type: ignore[misc]
def postgresql_conf(instance: "system.PostgreSQLInstance") -> Path:
    return instance.datadir / "postgresql.base.conf"


@hookimpl  # type: ignore[misc]
def postgresql_editable_conf(
    ctx: "BaseContext", instance: "system.PostgreSQLInstance"
) -> str:
    settings = available(ctx.settings)
    assert settings is not None
    patroni = impl.config(instance.qualname, settings)
    conf = pgtoolkit.conf.Configuration()
    with conf.edit() as entries:
        for k, v in patroni.postgresql.parameters.items():
            entries.add(k, v)
    return "".join(conf.lines)


@hookimpl  # type: ignore[misc]
def start_postgresql(
    ctx: "BaseContext", instance: "system.PostgreSQLInstance", foreground: bool
) -> Optional[Literal[True]]:
    """Start PostgreSQL with Patroni."""
    settings = available(ctx.settings)
    assert settings is not None
    impl.start(ctx, instance.qualname, settings, foreground=foreground)
    return True


@hookimpl  # type: ignore[misc]
def stop_postgresql(
    ctx: "BaseContext", instance: "system.PostgreSQLInstance"
) -> Optional[Literal[True]]:
    """Stop PostgreSQL through Patroni."""
    settings = available(ctx.settings)
    assert settings is not None
    impl.stop(ctx, instance.qualname, settings)
    return True


@hookimpl  # type: ignore[misc]
def restart_postgresql(
    ctx: "BaseContext", instance: "system.Instance"
) -> Optional[Literal[True]]:
    """Restart PostgreSQL with Patroni."""
    settings = available(ctx.settings)
    assert settings is not None
    impl.restart(ctx, instance, settings)
    return True


@hookimpl  # type: ignore[misc]
def reload_postgresql(
    ctx: "BaseContext", instance: system.Instance
) -> Optional[Literal[True]]:
    settings = available(ctx.settings)
    assert settings is not None
    impl.reload(ctx, instance, settings)
    return True


@hookimpl  # type: ignore[misc]
def promote_postgresql() -> None:
    raise exceptions.UnsupportedError(
        "unsupported operation: instance managed by Patroni"
    )


@hookimpl(trylast=True)  # type: ignore[misc]
def postgresql_service_name() -> str:
    return "patroni"


@hookimpl  # type: ignore[misc]
def instance_drop(ctx: "BaseContext", instance: "system.Instance") -> None:
    """Uninstall Patroni from an instance being dropped."""
    settings = available(ctx.settings)
    assert settings is not None
    s = service(instance)
    impl.delete(ctx, instance.qualname, s.cluster, settings)


@hookimpl  # type: ignore[misc]
def instance_env(ctx: "BaseContext", instance: "system.Instance") -> Dict[str, str]:
    settings = available(ctx.settings)
    assert settings is not None
    s = service(instance)
    configpath = impl._configpath(instance.qualname, settings)
    assert configpath.exists()
    return {
        "PATRONI_NAME": s.node,
        "PATRONI_SCOPE": s.cluster,
        "PATRONICTL_CONFIG_FILE": str(configpath),
    }


@hookimpl  # type: ignore[misc]
def cli() -> "click.Group":
    from .cli import cli as patroni

    return patroni
