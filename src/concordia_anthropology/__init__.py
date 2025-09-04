
from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("concordia_anthropology")
except PackageNotFoundError:  # during editable dev before install
    __version__ = "0.0.0"
__all__ = ["__version__"]
