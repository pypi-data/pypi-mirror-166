import logging
import sys
from typing import TYPE_CHECKING, Optional

from . import systemd, util
from .ctx import BaseContext
from .task import task

if TYPE_CHECKING:
    from .settings import SystemdSettings

logger = logging.getLogger(__name__)
POSTGRESQL_SERVICE_NAME = "pglift-postgresql@.service"
BACKUP_SERVICE_NAME = "pglift-backup@.service"
BACKUP_TIMER_NAME = "pglift-backup@.timer"


@task("installing systemd template unit for PostgreSQL")
def postgresql_systemd_unit_template(
    ctx: BaseContext,
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    settings = ctx.settings.postgresql
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    content = systemd.template(POSTGRESQL_SERVICE_NAME).format(
        executeas=systemd.executeas(ctx.settings),
        python=sys.executable,
        environment=environment,
        pid_directory=settings.pid_directory,
    )
    systemd.install(
        POSTGRESQL_SERVICE_NAME,
        util.with_header(content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@postgresql_systemd_unit_template.revert(
    "uninstalling systemd template unit for PostgreSQL"
)
def revert_postgresql_systemd_unit_template(
    ctx: BaseContext,
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    systemd.uninstall(
        POSTGRESQL_SERVICE_NAME, systemd_settings.unit_path, logger=logger
    )


@task("installing systemd template unit and timer for PostgreSQL backups")
def postgresql_backup_systemd_templates(
    ctx: BaseContext, *, env: Optional[str] = None, header: str = ""
) -> None:
    assert ctx.settings.systemd is not None
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    service_content = systemd.template(BACKUP_SERVICE_NAME).format(
        executeas=systemd.executeas(ctx.settings),
        environment=environment,
        python=sys.executable,
    )
    systemd.install(
        BACKUP_SERVICE_NAME,
        util.with_header(service_content, header),
        ctx.settings.systemd.unit_path,
        logger=logger,
    )
    timer_content = systemd.template(BACKUP_TIMER_NAME).format(
        # TODO: use a setting for that value
        calendar="daily",
    )
    systemd.install(
        BACKUP_TIMER_NAME,
        util.with_header(timer_content, header),
        ctx.settings.systemd.unit_path,
        logger=logger,
    )


@postgresql_backup_systemd_templates.revert(
    "uninstalling systemd template unit and timer for PostgreSQL backups"
)
def revert_postgresql_backup_systemd_templates(
    ctx: BaseContext, *, env: Optional[str] = None, header: str = ""
) -> None:
    assert ctx.settings.systemd is not None
    systemd.uninstall(
        BACKUP_SERVICE_NAME, ctx.settings.systemd.unit_path, logger=logger
    )
    systemd.uninstall(BACKUP_TIMER_NAME, ctx.settings.systemd.unit_path, logger=logger)


def do(ctx: BaseContext, env: Optional[str] = None, header: str = "") -> bool:
    if ctx.settings.service_manager != "systemd":
        logger.warning("not using systemd as 'service_manager', skipping installation")
        return False
    systemd_settings = ctx.settings.systemd
    assert systemd_settings is not None
    postgresql_systemd_unit_template(ctx, systemd_settings, env=env, header=header)
    ctx.hook.install_systemd_unit_template(
        ctx=ctx, systemd_settings=systemd_settings, header=header
    )
    postgresql_backup_systemd_templates(ctx, env=env, header=header)
    systemd.daemon_reload(ctx)
    return True


def undo(ctx: BaseContext) -> bool:
    if ctx.settings.service_manager != "systemd":
        logger.warning(
            "not using systemd as 'service_manager', skipping uninstallation"
        )
        return False
    systemd_settings = ctx.settings.systemd
    assert systemd_settings is not None
    revert_postgresql_backup_systemd_templates(ctx)
    ctx.hook.uninstall_systemd_unit_template(ctx=ctx, systemd_settings=systemd_settings)
    revert_postgresql_systemd_unit_template(ctx, systemd_settings)
    systemd.daemon_reload(ctx)
    return True
