__all__ = ["Settings"]

import tomllib as tomlreader
from enum import Enum
from pathlib import Path
from typing import ClassVar, Self

import tomli_w as tomlwriter
from pydantic import BaseModel

from freyr import get_config


class SettingsModel(
    BaseModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="ignore",
):
    pass


class Source(str, Enum):
    POSTGRES = "POSTGRES"
    SQLITE = "SQLITE"


class DatabaseSettings(SettingsModel):
    host: str = ""
    name: str = "freyr.sqlite"
    password: str = ""
    source: Source = Source.SQLITE
    user: str = ""

    @property
    def db_url(self: Self) -> str:
        if self.source == Source.POSTGRES:
            return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.name}"
        return f"sqlite:///{self.name}"


class WebsiteSettings(SettingsModel):
    host: str = "127.0.0.1"
    port: int = 25710
    reload: bool = False


class Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config() / "settings.toml"
    database: DatabaseSettings = DatabaseSettings()
    website: WebsiteSettings = WebsiteSettings()

    @classmethod
    def load(cls: type[Self]) -> Self:
        if not cls._filepath.exists():
            cls().save()
        with cls._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return cls(**content)

    def save(self: Self) -> Self:
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self
