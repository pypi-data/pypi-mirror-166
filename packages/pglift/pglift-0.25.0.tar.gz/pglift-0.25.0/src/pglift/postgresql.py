import enum
import logging
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Dict, Optional, Type

import psycopg.conninfo
from pydantic import Field, SecretStr, validator

from . import hookimpl
from ._compat import Literal
from .types import AnsibleConfig, AutoStrEnum, CLIConfig, Manifest

if TYPE_CHECKING:
    from .models import interface, system
    from .settings import Settings

logger = logging.getLogger(__name__)


@hookimpl(trylast=True)  # type: ignore[misc]
def postgresql_service_name() -> str:
    return "postgresql"


class Standby(Manifest):
    """Standby information."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "status": {"hide": True},
        "replication_lag": {"hide": True},
    }
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {
        "replication_lag": {"hide": True}
    }

    @enum.unique
    class State(AutoStrEnum):
        """Instance standby status"""

        demoted = enum.auto()
        promoted = enum.auto()

    for_: str = Field(
        alias="for",
        description="DSN of primary for streaming replication.",
    )
    password: Optional[SecretStr] = Field(
        default=None, description="Password for the replication user.", exclude=True
    )
    status: State = Field(
        default=State.demoted, description=("Instance standby state.")
    )
    slot: Optional[str] = Field(
        description="Replication slot name. Must exist on primary."
    )
    replication_lag: Optional[Decimal] = Field(
        default=None, description="Replication lag.", readOnly=True
    )

    @validator("for_")
    def __validate_for_(cls, value: str) -> str:
        """Validate 'for' field.

        >>> Standby.parse_obj({"for": "host=localhost"})
        Standby(for_='host=localhost', password=None, status=<State.demoted: 'demoted'>, slot=None, replication_lag=None)
        >>> Standby.parse_obj({"for": "hello"})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Standby
        for
          missing "=" after "hello" in connection info string
         (type=value_error)
        >>> Standby.parse_obj({"for": "host=localhost password=xx"})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Standby
        for
          connection string must not contain a password (type=value_error)
        """
        try:
            conninfo = psycopg.conninfo.conninfo_to_dict(value)
        except psycopg.ProgrammingError as e:
            raise ValueError(str(e))
        if "password" in conninfo:
            raise ValueError("connection string must not contain a password")
        return value

    @property
    def primary_conninfo(self) -> str:
        """Connection string to the primary.

        >>> s = Standby.parse_obj({"for": "host=primary port=5444", "password": "qwerty"})
        >>> s.primary_conninfo
        'host=primary port=5444 password=qwerty'
        """
        kw = {}
        if self.password:
            kw["password"] = self.password.get_secret_value()
        return psycopg.conninfo.make_conninfo(self.for_, **kw)


@hookimpl(trylast=True)  # type: ignore[misc]
def standby_model() -> Type[Standby]:
    return Standby


@hookimpl(trylast=True)  # type: ignore[misc]
def postgresql_conf(instance: "system.PostgreSQLInstance") -> Path:
    return instance.datadir / "postgresql.conf"


@hookimpl(trylast=True)  # type: ignore[misc]
def postgresql_editable_conf(instance: "system.PostgreSQLInstance") -> str:
    return "".join(instance.config(managed_only=True).lines)


@hookimpl(trylast=True)  # type: ignore[misc]
def configure_auth(
    settings: "Settings",
    instance: "system.BaseInstance",
    manifest: "interface.Instance",
) -> Literal[True]:
    """Configure authentication for the PostgreSQL instance."""
    logger.info("configuring PostgreSQL authentication")
    hba_path = instance.datadir / "pg_hba.conf"
    hba = manifest.pg_hba(settings)
    hba_path.write_text(hba)

    ident_path = instance.datadir / "pg_ident.conf"
    ident = manifest.pg_ident(settings)
    ident_path.write_text(ident)
    return True
