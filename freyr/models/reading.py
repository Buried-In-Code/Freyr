__all__ = ["Reading", "ReadingEntry", "ReadingInput"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel


class BaseReading(BaseModel):
    timestamp: datetime | None = None
    temperature: Decimal | None = None
    humidity: Decimal | None = None

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, BaseReading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, BaseReading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.timestamp))


class Reading(BaseReading):
    id: int


class ReadingEntry(BaseReading):
    id: int


class ReadingInput(BaseReading):
    pass
