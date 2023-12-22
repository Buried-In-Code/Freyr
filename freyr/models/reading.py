__all__ = ["Reading", "ReadingEntry", "ReadingInput"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel


class BaseReading(BaseModel):
    temperature: Decimal
    humidity: Decimal


class Reading(BaseReading):
    id: int  # noqa: A003
    timestamp: datetime

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Reading):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.timestamp))


class ReadingEntry(BaseReading):
    id: int  # noqa: A003
    timestamp: datetime

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, ReadingEntry):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, ReadingEntry):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.timestamp))


class ReadingInput(BaseReading):
    pass
