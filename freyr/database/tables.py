__all__ = ["db", "Device", "Entry"]

from datetime import datetime
from decimal import Decimal

from pony.orm import Database, PrimaryKey, Required, Set, composite_key

from freyr.models import Device as DeviceModel, Entry as EntryModel

db = Database()

class Device(db.Entity):
    _table_ = "devices"

    device_id: int = PrimaryKey(int, auto=True)
    name: str = Required(str, unique=True)
    entries: list["Entry"] = Set("Entry")

    def to_model(self) -> DeviceModel:
        return DeviceModel(
            name = self.name,
            entries = reversed(sorted({x.to_model() for x in self.entries})),
        )

class Entry(db.Entity):
    _table_ = "entries"

    entry_id: int = PrimaryKey(int, auto=True)
    device: Device = Required(Device)
    timestamp: datetime = Required(datetime)
    temperature: Decimal = Required(Decimal)
    humidity: Decimal = Required(Decimal)

    composite_key(device, timestamp)

    def to_model(self) -> EntryModel:
        return EntryModel(
            timestamp = self.timestamp,
            temperature = self.temperature,
            humidity = self.humidity,
        )
