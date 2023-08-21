__all__ = ["db", "Device", "Reading"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pony.orm import Database, PrimaryKey, Required, Set, composite_key

from freyr.models import DeviceModel, LatestModel, ReadingModel

db = Database()


class Device(db.Entity):
    _table_ = "devices"

    device_id: int = PrimaryKey(int, auto=True)
    name: str = Required(str, unique=True)
    readings: list["Reading"] = Set("Reading")

    def to_model(self: Self) -> DeviceModel:
        return DeviceModel(
            name=self.name,
            readings=sorted({x.to_model() for x in self.readings}, reverse=True),
        )

    def to_latest(self: Self) -> LatestModel:
        readings = sorted({x.to_model() for x in self.readings}, reverse=True)
        return LatestModel(
            name=self.name,
            reading=readings[0] if readings else None,
        )


class Reading(db.Entity):
    _table_ = "readings"

    reading_id: int = PrimaryKey(int, auto=True)
    device: Device = Required(Device)
    _timestamp: datetime = Required(datetime, column="timestamp")
    temperature: Decimal = Required(Decimal)
    humidity: Decimal = Required(Decimal)

    composite_key(device, _timestamp)

    @property
    def timestamp(self: Self) -> datetime:
        if isinstance(self._timestamp, str):
            return datetime.strptime(self._timestamp, "%Y-%m-%d %H:%M:%S%z").astimezone()
        return self._timestamp.astimezone()

    @timestamp.setter
    def timestamp(self: Self, value: datetime) -> None:
        self._timestamp = value

    def to_model(self: Self) -> ReadingModel:
        return ReadingModel(
            timestamp=self.timestamp,
            temperature=self.temperature,
            humidity=self.humidity,
        )
