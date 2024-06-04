__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pony.orm import db_session, flush

from freyr.database.tables import Device, Reading
from freyr.models import Summary
from freyr.models.reading import Reading as ReadingModel, ReadingEntry, ReadingInput
from freyr.responses import ErrorResponse
from freyr.utils import (
    get_daily_avg_readings,
    get_daily_high_readings,
    get_daily_low_readings,
    get_hourly_avg_readings,
    get_hourly_high_readings,
    get_hourly_low_readings,
    get_monthly_avg_readings,
    get_monthly_high_readings,
    get_monthly_low_readings,
    get_yearly_avg_readings,
    get_yearly_high_readings,
    get_yearly_low_readings,
)

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/{device_id}/readings",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)


def get_device(device_id: int) -> Device:
    if resource := Device.get(id=device_id):
        return resource
    raise HTTPException(status_code=404, detail="Device not found.")


@router.get(path="")
def list_endpoint(*, device_id: int, limit: int = 100, offset: int = 0) -> list[ReadingEntry]:
    with db_session:
        device = get_device(device_id=device_id)
        resources = device.readings

        return sorted((x.to_entry_model() for x in resources), reverse=True)[
            offset : offset + limit
        ]


@router.post(path="", status_code=201)
def create_endpoint(*, device_id: int, body: ReadingInput) -> ReadingModel:
    with db_session:
        device = get_device(device_id=device_id)
        resource = Reading(
            device=device,
            timestamp=body.timestamp
            or datetime.fromisoformat(datetime.now().isoformat(timespec="seconds")),
            temperature=body.temperature,
            humidity=body.humidity,
        )
        flush()

        return resource.to_model()


@router.get(path="/yearly")
def yearly_readings(*, device_id: int, limit: int = 100, offset: int = 0) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_yearly_high_readings(entries=device.readings)[offset : offset + limit],
            averages=get_yearly_avg_readings(entries=device.readings)[offset : offset + limit],
            lows=get_yearly_low_readings(entries=device.readings)[offset : offset + limit],
        )


@router.get(path="/monthly")
def monthly_readings(
    *, device_id: int, year: int | None = None, limit: int = 100, offset: int = 0
) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_monthly_high_readings(entries=device.readings, year=year)[
                offset : offset + limit
            ],
            averages=get_monthly_avg_readings(entries=device.readings, year=year)[
                offset : offset + limit
            ],
            lows=get_monthly_low_readings(entries=device.readings, year=year)[
                offset : offset + limit
            ],
        )


@router.get(path="/daily")
def daily_readings(
    *,
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_daily_high_readings(entries=device.readings, year=year, month=month)[
                offset : offset + limit
            ],
            averages=get_daily_avg_readings(entries=device.readings, year=year, month=month)[
                offset : offset + limit
            ],
            lows=get_daily_low_readings(entries=device.readings, year=year, month=month)[
                offset : offset + limit
            ],
        )


@router.get(path="/hourly")
def hourly_readings(
    *,
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_hourly_high_readings(
                entries=device.readings, year=year, month=month, day=day
            )[offset : offset + limit],
            averages=get_hourly_avg_readings(
                entries=device.readings, year=year, month=month, day=day
            )[offset : offset + limit],
            lows=get_hourly_low_readings(entries=device.readings, year=year, month=month, day=day)[
                offset : offset + limit
            ],
        )
