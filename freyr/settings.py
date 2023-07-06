__all__ = ["Settings"]

import tomllib as tomlreader
from pathlib import Path
from typing import ClassVar, Self

import tomli_w as tomlwriter
from pydantic import BaseModel

from freyr import get_config_root


class SettingsModel(
    BaseModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="ignore",
):
    pass


class DatabaseSettings(SettingsModel):
    name: str = "freyr.sqlite"


class WebsiteSettings(SettingsModel):
    host: str = "127.0.0.1"
    port: int = 25710
    reload: bool = False


class _Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    _instance: ClassVar["_Settings"] = None
    database: DatabaseSettings = DatabaseSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls) -> Self:
        if not cls._filepath.exists():
            _Settings().save()
        with cls._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return _Settings(**content)

    def save(self) -> Self:
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self


def Settings() -> _Settings:  # noqa: N802
    if _Settings._instance is None:
        _Settings._instance = _Settings.load()
    return _Settings._instance
