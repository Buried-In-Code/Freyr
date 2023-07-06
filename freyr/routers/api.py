__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Body, Query, HTTPException
from pony.orm import db_session

from freyr.database.tables import Device, Entry
from freyr.models import Device as DeviceModel, Entry as EntryModel
from freyr.responses import ErrorResponse

router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
devices_router = APIRouter(prefix="/devices", tags=["Devices"])


@devices_router.post(path="", status_code=204)
def add_stat(entry: EntryModel, device: Annotated[str, Body()]) -> None:
    with db_session:
        _device = Device.get(name=device)
        if not _device:
            _device = Device(name=device)
        Entry(
            device=_device,
            timestamp=entry.timestamp,
            temperature=entry.temperature,
            humidity=entry.humidity,
        )


@devices_router.get(path="")
def list_devices(name: str | None = None) -> list[DeviceModel]:
    with db_session:
        devices = Device.select()
        if name:
            devices = [
                x
                for x in devices
                if x.name.casefold() in name.casefold() or name.casefold() in x.name.casefold()
            ]
        return sorted({x.to_model() for x in devices})


@devices_router.get(path="/{device_id}")
def get_device(device_id: int) -> DeviceModel:
    with db_session:
        device = Device.get(device_id=device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found.")
        return device.to_model()


router.include_router(devices_router)
