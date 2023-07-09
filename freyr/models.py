__all__ = ["Device", "Entry", "NewEntry"]

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Entry(BaseModel):
    timestamp: datetime
    temperature: Decimal
    humidity: Decimal

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Entry):
            raise NotImplementedError
        return self.timestamp < other.timestamp

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Entry):
            raise NotImplementedError
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


class Device(BaseModel, populate_by_name=True):
    name: str
    entries: list[Entry] = Field(default_factory=list)

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Device):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Device):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))


class NewEntry(BaseModel):
    device: str
    temperature: Decimal
    humidity: Decimal
