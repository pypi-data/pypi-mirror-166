import pluggy

from . import _compat, pm, settings

__all__ = ["hookimpl"]

hookimpl = pluggy.HookimplMarker(__name__)


def version() -> str:
    return _compat.version(__name__)


def plugin_manager(s: settings.Settings) -> pm.PluginManager:
    return pm.PluginManager.get(s)
