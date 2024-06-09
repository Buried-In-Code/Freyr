from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional, Self

from sqlmodel import Field, Relationship, SQLModel


class DeviceBase(SQLModel):
    name: str = Field(index=True)


class Device(DeviceBase, table=True):
    __tablename__ = "devices"

    id: int | None = Field(default=None, primary_key=True)
    readings: list["Reading"] = Relationship(
        back_populates="device", sa_relationship_kwargs={"order_by": "Reading.timestamp.desc()"}
    )

    def __lt__(self: Self, other) -> int:  # noqa: ANN001
        if not isinstance(other, Device):
            raise NotImplementedError
        return self.name < other.name

    def __eq__(self: Self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, Device):
            raise NotImplementedError
        return self.name == other.name

    def __hash__(self: Self) -> int:
        return hash((type(self), self.name))


class DeviceCreate(DeviceBase):
    pass


class DevicePublic(DeviceBase):
    id: int
    reading: Optional["ReadingPublic"] = None


class DeviceWithReadings(DeviceBase):
    id: int
    readings: list["ReadingPublic"] = Field(default_factory=list)


class ReadingBase(SQLModel):
    temperature: Decimal | None = None
    humidity: Decimal | None = None


class Reading(ReadingBase, table=True):
    __tablename__ = "readings"

    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime
    device_id: int = Field(foreign_key="devices.id")
    device: Device = Relationship(back_populates="readings")

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


class ReadingCreate(ReadingBase):
    device_id: int | None = None
    timestamp: datetime | None = None


class ReadingPublic(ReadingBase):
    id: int
    timestamp: datetime


class Summary(SQLModel):
    class Reading(SQLModel):
        timestamp: datetime
        temperature: Annotated[Decimal, Field(decimal_places=2)] | None = None
        humidity: Annotated[Decimal, Field(decimal_places=2)] | None = None

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
