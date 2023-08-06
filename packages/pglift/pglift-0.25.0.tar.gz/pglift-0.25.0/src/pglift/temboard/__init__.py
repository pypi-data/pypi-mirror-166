import logging
from typing import TYPE_CHECKING, Optional, Type

import click
import pydantic

from .. import exceptions, hookimpl, systemd, util
from ..models import interface, system
from . import impl, models
from .impl import available as available

if TYPE_CHECKING:
    from pgtoolkit.conf import Configuration

    from ..ctx import BaseContext
    from ..settings import Settings, SystemdSettings

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl  # type: ignore[misc]
def system_lookup(
    ctx: "BaseContext", instance: "system.PostgreSQLInstance"
) -> Optional[models.Service]:
    settings = available(ctx.settings)
    assert settings is not None
    try:
        p = impl.port(instance.qualname, settings)
        passwd = impl.password(instance.qualname, settings)
    except exceptions.FileNotFoundError as exc:
        logger.debug("failed to read temboard-agent port for %s: %s", instance, exc)
        return None
    else:
        password = None
        if passwd is not None:
            password = pydantic.SecretStr(passwd)
        return models.Service(port=p, password=password)


@hookimpl  # type: ignore[misc]
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl  # type: ignore[misc]
def get(
    ctx: "BaseContext", instance: "system.Instance"
) -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(port=s.port)


SYSTEMD_SERVICE_NAME = "pglift-temboard_agent@.service"


@hookimpl  # type: ignore[misc]
def install_systemd_unit_template(
    ctx: "BaseContext", systemd_settings: "SystemdSettings", header: str = ""
) -> None:
    logger.info("installing systemd template unit for Temboard Agent")
    settings = available(ctx.settings)
    assert settings is not None
    configpath = str(settings.configpath).replace("{name}", "%i")
    content = systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(ctx.settings),
        configpath=configpath,
        execpath=str(settings.execpath),
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
    logger.info("uninstalling systemd template unit for Temboard Agent")
    systemd.uninstall(SYSTEMD_SERVICE_NAME, systemd_settings.unit_path, logger=logger)


@hookimpl  # type: ignore[misc]
def instance_configure(
    ctx: "BaseContext", manifest: "interface.Instance", config: "Configuration"
) -> None:
    """Install temboard agent for an instance when it gets configured."""
    settings = available(ctx.settings)
    if not settings:
        logger.warning("temboard not available, skipping agent configuration")
        return
    impl.setup(ctx, manifest, settings, config)


@hookimpl  # type: ignore[misc]
def instance_start(ctx: "BaseContext", instance: "system.Instance") -> None:
    """Start temboard agent service."""
    settings = available(ctx.settings)
    if not settings or not impl.enabled(instance.qualname, settings):
        return
    impl.start(ctx, instance.qualname, settings)


@hookimpl  # type: ignore[misc]
def instance_stop(ctx: "BaseContext", instance: "system.Instance") -> None:
    """Stop temboard agent service."""
    settings = available(ctx.settings)
    if not settings or not impl.enabled(instance.qualname, settings):
        return
    impl.stop(ctx, instance.qualname, settings)


@hookimpl  # type: ignore[misc]
def instance_drop(ctx: "BaseContext", instance: "system.Instance") -> None:
    """Uninstall temboard from an instance being dropped."""
    settings = available(ctx.settings)
    if not settings:
        return
    manifest = interface.Instance(name=instance.name, version=instance.version)
    impl.revert_setup(ctx, manifest, settings, instance.config())


@hookimpl  # type: ignore[misc]
def rolename(settings: "Settings") -> str:
    assert settings.temboard
    return settings.temboard.role


@hookimpl  # type: ignore[misc]
def role(settings: "Settings", manifest: "interface.Instance") -> "interface.Role":
    name = rolename(settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    assert service_manifest is not None
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    return interface.Role(
        name=name,
        password=password,
        login=True,
        superuser=True,
    )


@hookimpl  # type: ignore[misc]
def cli() -> "click.Group":
    from .cli import temboard_agent

    return temboard_agent
