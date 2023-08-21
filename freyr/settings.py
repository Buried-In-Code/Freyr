__all__ = ["Settings"]

from pathlib import Path
from typing import ClassVar

import tomli_w as tomlwriter
from pydantic import BaseModel

from freyr import get_config_root

try:
    import tomllib as tomlreader  # Python >= 3.11
except ModuleNotFoundError:
    import tomli as tomlreader  # Python < 3.11


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


class Settings(SettingsModel):
    _filepath: ClassVar[Path] = get_config_root() / "settings.toml"
    database: DatabaseSettings = DatabaseSettings()
    website: WebsiteSettings = WebsiteSettings()

    @staticmethod
    def load() -> "Settings":
        if not Settings._filepath.exists():
            Settings().save()
        with Settings._filepath.open("rb") as stream:
            content = tomlreader.load(stream)
        return Settings(**content)

    def save(self: "Settings") -> "Settings":
        with self._filepath.open("wb") as stream:
            content = self.model_dump(by_alias=False)
            tomlwriter.dump(content, stream)
        return self
