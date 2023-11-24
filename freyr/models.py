__all__ = ["DeviceModel", "SummaryModel", "ReadingModel", "NewReading"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, Field


class ReadingModel(BaseModel):
    timestamp: datetime
    temperature: Decimal
    humidity: Decimal

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, ReadingModel):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, ReadingModel):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self: Self) -> int:
        return hash((type(self), self.timestamp))


class DeviceModel(BaseModel):
    name: str
    readings: list[ReadingModel] = Field(default_factory=list)

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, DeviceModel):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, DeviceModel):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self: Self) -> int:
        return hash((type(self), self.name))


class SummaryModel(BaseModel):
    name: str
    highs: list[ReadingModel] = Field(default_factory=list)
    averages: list[ReadingModel] = Field(default_factory=list)
    lows: list[ReadingModel] = Field(default_factory=list)

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, SummaryModel):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, SummaryModel):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self: Self) -> int:
        return hash((type(self), self.name))


class NewReading(BaseModel):
    device: str
    temperature: Decimal
    humidity: Decimal
