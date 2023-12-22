__all__ = ["Device", "DeviceEntry", "DeviceInput"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, Field


class BaseDevice(BaseModel):
    name: str

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, BaseDevice):
            raise NotImplementedError
        return self.name.casefold() < other.name.casefold()

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, BaseDevice):
            raise NotImplementedError
        return self.name.casefold() == other.name.casefold()

    def __hash__(self: Self) -> int:
        return hash((type(self), self.name.casefold()))


class Device(BaseDevice):
    class Reading(BaseModel):
        id: int  # noqa: A003
        timestamp: datetime
        temperature: Decimal
        humidity: Decimal

        def __lt__(self: Self, other) -> int:  # noqa: ANN001
            if not isinstance(other, Device.Reading):
                raise NotImplementedError
            return self.timestamp < other.timestamp

        def __eq__(self: Self, other) -> bool:  # noqa: ANN001
            if not isinstance(other, Device.Reading):
                raise NotImplementedError
            return self.timestamp == other.timestamp

        def __hash__(self: Self) -> int:
            return hash((type(self), self.timestamp))

    id: int  # noqa: A003
    readings: list[Reading] = Field(default_factory=list)


class DeviceEntry(BaseDevice):
    id: int  # noqa: A003


class DeviceInput(BaseDevice):
    pass
