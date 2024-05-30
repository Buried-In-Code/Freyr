__all__ = ["db", "Device", "Reading"]

from datetime import datetime
from decimal import Decimal
from typing import Self

from pony.orm import Database, Optional, PrimaryKey, Required, Set, composite_key

from freyr.models.device import Device as DeviceModel, DeviceEntry
from freyr.models.reading import Reading as ReadingModel, ReadingEntry

db = Database()


class Device(db.Entity):
    _table_ = "devices"

    id: int = PrimaryKey(int, auto=True)
    name: str = Required(str, unique=True)
    readings: list["Reading"] = Set("Reading")

    def to_entry_model(self: Self) -> DeviceEntry:
        return DeviceEntry(id=self.id, name=self.name)

    def to_model(self: Self) -> DeviceModel:
        return DeviceModel(
            id=self.id,
            name=self.name,
            readings=list(
                {
                    DeviceModel.Reading(
                        id=x.id,
                        timestamp=x.timestamp,
                        temperature=x.temperature,
                        humidity=x.humidity,
                    )
                    for x in self.readings
                }
            ),
        )


class Reading(db.Entity):
    _table_ = "readings"

    id: int = PrimaryKey(int, auto=True)
    device: Device = Required(Device)
    timestamp: datetime = Required(datetime)
    temperature: Decimal | None = Optional(Decimal, nullable=True)
    humidity: Decimal | None = Optional(Decimal, nullable=True)

    composite_key(device, timestamp)

    def to_entry_model(self: Self) -> ReadingEntry:
        return ReadingEntry(
            id=self.id,
            timestamp=self.timestamp,
            temperature=self.temperature,
            humidity=self.humidity,
        )

    def to_model(self: Self) -> ReadingModel:
        return ReadingModel(
            id=self.id,
            timestamp=self.timestamp,
            temperature=self.temperature,
            humidity=self.humidity,
        )
