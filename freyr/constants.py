__all__ = ["constants"]

from functools import cached_property
from typing import Self

from freyr.models.reading import Reading
from freyr.settings import Settings


class Constants:
    @cached_property
    def cache(self: Self) -> dict[int, Reading]:
        return {}

    @cached_property
    def settings(self: Self) -> Settings:
        return Settings.load().save()


constants = Constants()
