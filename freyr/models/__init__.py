__all__ = ["Summary"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, Field


class Summary(BaseModel):
    class Reading(BaseModel):
        timestamp: datetime
        temperature: Decimal
        humidity: Decimal

        def __lt__(self: Self, other) -> int:  # noqa: ANN001
            if not isinstance(other, Summary.Reading):
                raise NotImplementedError
            return self.timestamp < other.timestamp

        def __eq__(self: Self, other) -> bool:  # noqa: ANN001
            if not isinstance(other, Summary.Reading):
                raise NotImplementedError
            return self.timestamp == other.timestamp

        def __hash__(self: Self) -> int:
            return hash((type(self), self.timestamp))

    highs: list[Reading] = Field(default_factory=list)
    averages: list[Reading] = Field(default_factory=list)
    lows: list[Reading] = Field(default_factory=list)
