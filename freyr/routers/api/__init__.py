__all__ = ["router"]

import logging
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter
from pony.orm import db_session, flush
from pydantic import BaseModel

from freyr.constants import constants
from freyr.database.tables import Device, Reading
from freyr.responses import ErrorResponse
from freyr.routers.api.device import router as device_router

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
router.include_router(device_router)


class NewReading(BaseModel):
    device: str
    temperature: Decimal
    humidity: Decimal


@router.post(path="/readings", status_code=204)
def add_reading(reading: NewReading):  # noqa: ANN202
    with db_session:
        device = Device.get(name=reading.device) or Device(name=reading.device)
        reading = Reading(
            device=device,
            timestamp=datetime.fromisoformat(datetime.now().isoformat(timespec="seconds")),
            temperature=reading.temperature,
            humidity=reading.humidity,
        )
        flush()
        constants.cache[device.id] = reading.to_model()
