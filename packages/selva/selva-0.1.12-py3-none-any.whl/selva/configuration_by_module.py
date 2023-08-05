import importlib
import inspect
import os
from pathlib import Path
from typing import Any
from types import ModuleType

__all__ = ("Settings",)

CONFIGURATION_PACKAGE = "configuration"
CONFIGURATION_MODULE = f"{CONFIGURATION_PACKAGE}.settings"
ACTIVE_ENV = "SELVA_ENV"


def get_valid_settings(settings: ModuleType) -> dict[str, Any]:
    return {
        name: value
        for name, value in inspect.getmembers(settings)
        if name[0].isalpha() and all(i.isupper() or i == "_" for i in name)
    }


def get_settings() -> dict[str, Any]:
    try:
        settings_module = importlib.import_module(CONFIGURATION_MODULE)
        settings = get_valid_settings(settings_module)
    except ImportError:
        settings = {}

    if active_env := os.getenv(ACTIVE_ENV, None):
        try:
            env_settings_module = importlib.import_module(f"{CONFIGURATION_MODULE}_{active_env}")
            env_settings = get_valid_settings(env_settings_module)
        except ImportError:
            raise ValueError(f"settings module for environment {active_env} not found")

        settings |= env_settings

    return settings


class Settings:
    def __init__(self, initial: dict = None):
        self._data = get_settings()
        if initial:
            self._data |= initial

    def __getattr__(self, name: str) -> Any | None:
        return self._data.get(name)

    @property
    def resources_path(self) -> Path:
        return Path(os.getcwd()) / "resources"

    def get_resource_path(self, *args: str) -> Path:
        resources = self.resources_path
        return resources.joinpath(*args)
