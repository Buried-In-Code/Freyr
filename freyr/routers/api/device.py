__all__ = ["router"]

import logging

from fastapi import APIRouter, HTTPException
from pony.orm import db_session, flush

from freyr.database.tables import Device
from freyr.models.device import Device as DeviceModel, DeviceEntry, DeviceInput
from freyr.responses import ErrorResponse
from freyr.routers.api.reading import router as readings_router

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/devices", responses={422: {"description": "Validation error", "model": ErrorResponse}}
)


@router.get(path="")
def list_endpoint(*, name: str | None = None) -> list[DeviceEntry]:
    with db_session:
        resources = Device.select()
        if name:
            resources = [x for x in resources if x.name in name or name in x.name]

        return sorted(x.to_entry_model() for x in resources)


@router.post(path="", status_code=201)
def create_endpoint(*, body: DeviceInput) -> DeviceModel:
    with db_session:
        if Device.get(name=body.name):
            raise HTTPException(status_code=409, detail="Device already exists.")
        resource = Device(name=body.name)
        flush()

        return resource.to_model()


def get_resource(device_id: int) -> Device:
    if resource := Device.get(id=device_id):
        return resource
    raise HTTPException(status_code=404, detail="Device not found.")


@router.get(path="/{device_id}")
def get_endpoint(*, device_id: int) -> DeviceModel:
    with db_session:
        return get_resource(device_id=device_id).to_model()


@router.put(path="/{device_id}")
def update_endpoint(*, device_id: int, body: DeviceInput) -> DeviceModel:
    with db_session:
        resource = get_resource(device_id=device_id)
        exists = Device.get(name=body.name)
        if exists and exists != resource:
            raise HTTPException(status_code=409, detail="Device already exists.")

        resource.name = body.name
        flush()

        return resource.to_model()


@router.delete(path="/{device_id}", status_code=204)
def delete_endpoint(*, device_id: int) -> None:
    with db_session:
        resource = get_resource(device_id=device_id)
        resource.delete()


router.include_router(readings_router)
