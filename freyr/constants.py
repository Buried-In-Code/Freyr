__all__ = ["constants"]

from functools import cached_property
from typing import Self

from freyr.settings import Settings


class Constants:
    @cached_property
    def settings(self: Self) -> Settings:
        return Settings.load().save()


constants = Constants()
