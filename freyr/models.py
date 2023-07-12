__all__ = ["DeviceModel", "LatestModel", "SummaryModel", "ReadingModel", "NewReading"]

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ReadingModel(BaseModel):
    timestamp: datetime
    temperature: Decimal
    humidity: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, ReadingModel):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, ReadingModel):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


class DeviceModel(BaseModel):
    name: str
    readings: list[ReadingModel] = Field(default_factory=list)

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, DeviceModel):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, DeviceModel):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))


class LatestModel(BaseModel):
    name: str
    reading: ReadingModel | None = None

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, LatestModel):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, LatestModel):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))


class SummaryModel(BaseModel):
    name: str
    highs: list[ReadingModel] = Field(default_factory=list)
    lows: list[ReadingModel] = Field(default_factory=list)

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, SummaryModel):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, SummaryModel):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))


class NewReading(BaseModel):
    device: str
    temperature: Decimal
    humidity: Decimal
