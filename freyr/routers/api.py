__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException
from pony.orm import db_session

from freyr.database.tables import Device, Entry
from freyr.models import Device as DeviceModel, NewEntry
from freyr.responses import ErrorResponse

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
devices_router = APIRouter(prefix="/devices", tags=["Devices"])


@devices_router.post(path="", status_code=204)
def add_stat(entry: NewEntry) -> None:
    with db_session:
        device = Device.get(name=entry.device)
        if not device:
            device = Device(name=entry.device)
        Entry(
            device=device,
            timestamp=datetime.now(),
            temperature=entry.temperature,
            humidity=entry.humidity,
        )


@devices_router.post(path="/error", status_code=204)
def device_error(error: str = Body(embed=True)) -> None:
    LOGGER.error(error)


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
