__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Body, Query
from pony.orm import db_session

from freyr.database.tables import Device, Entry
from freyr.models import Entry as EntryModel, Device as DeviceModel
from freyr.responses import ErrorResponse

router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
stat_router = APIRouter(prefix="/stats", tags=["Stats"])


@stat_router.post(path="", status_code=204)
def add_stat(entry: EntryModel, device: Annotated[str, Body()]) -> None:
    with db_session:
        _device = Device.get(name = device)
        if not _device:
            _device = Device(name = device)
        Entry(
            device = _device,
            timestamp = entry.timestamp,
            temperature = entry.temperature,
            humidity = entry.humidity,
        )


@stat_router.get(path="")
def list_stats(name: str = Query(alias = "device", default = "")) -> list[DeviceModel]:
    with db_session:
        devices = Device.select()
        if name:
            devices = [
                x for x in devices
                if x.name.casefold() in name.casefold() or name.casefold() in x.name.casefold()
            ]
        return sorted({x.to_model() for x in devices})


router.include_router(stat_router)
