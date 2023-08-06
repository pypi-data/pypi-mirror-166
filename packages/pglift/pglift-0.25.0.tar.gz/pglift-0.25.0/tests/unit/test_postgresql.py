from pglift.ctx import Context
from pglift.models import interface, system


def test_postgresql_conf(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_conf(instance=instance).name == "postgresql.conf"


def test_postgresql_editable_conf(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_editable_conf(ctx=ctx, instance=instance) == "\n".join(
        [
            "port = 999",
            "unix_socket_directories = /socks",
            "# backslash_quote = 'safe_encoding'",
        ]
    )


def test_configure_auth(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    hba = instance.datadir / "pg_hba.conf"
    ident = instance.datadir / "pg_ident.conf"
    orig_hba = hba.read_text()
    orig_ident = ident.read_text()
    ctx.hook.configure_auth(
        settings=ctx.settings, instance=instance, manifest=instance_manifest
    )
    assert hba.read_text() != orig_hba
    assert ident.read_text() != orig_ident
