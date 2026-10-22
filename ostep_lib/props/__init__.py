"""Reusable props for the OSTEP series (see CORE_API.md and ostep_lib/README.md).

* ``core``      shared props every episode uses (CPU, Memory, Disk, cards, ...)
* ``ov_*``      props introduced by episode 01-03 (Terminal, SystemStack, ...)
* ``p04_*`` ... props introduced by later episodes; every ``p*_*.py`` module in this
  folder is imported automatically and its ``__all__`` re-exported.
"""
import importlib as _importlib
import pkgutil as _pkgutil
import warnings as _warnings

from .core import *  # noqa: F401,F403
from .core import __all__ as _core_all

__all__ = list(_core_all)

_modules = sorted(m.name for m in _pkgutil.iter_modules(__path__))
for _name in _modules:
    if _name in ("core", "preview") or _name.endswith("preview") or not (_name.startswith("ov_") or (_name.startswith("p") and "_" in _name)):
        continue
    try:
        _mod = _importlib.import_module(f".{_name}", __name__)
    except Exception as _e:  # keep the library importable while a module is being edited
        _warnings.warn(f"ostep_lib.props: could not import {_name}: {_e!r}")
        continue
    for _n in getattr(_mod, "__all__", []):
        globals()[_n] = getattr(_mod, _n)
        if _n not in __all__:
            __all__.append(_n)
