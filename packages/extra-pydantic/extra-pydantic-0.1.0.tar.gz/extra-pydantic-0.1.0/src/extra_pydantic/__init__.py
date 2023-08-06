"""Parametrized Generic support for pydantic."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("extra-pydantic")
except PackageNotFoundError:
    __version__ = "uninstalled"

from .main import BaseModel, ModelMetaclass, create_model
from .monkeypatch import patched_pydantic_base_model

__all__ = ["BaseModel", "ModelMetaclass", "create_model", "patched_pydantic_base_model"]
