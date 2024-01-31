__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pony.orm import db_session, flush

from freyr.constants import constants
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
def list_endpoint(*, device_id: int) -> list[ReadingEntry]:
    with db_session:
        device = get_device(device_id=device_id)
        resources = device.readings

        return sorted(x.to_entry_model() for x in resources)


@router.post(path="", status_code=201)
def create_endpoint(*, device_id: int, body: ReadingInput) -> ReadingModel:
    with db_session:
        device = get_device(device_id=device_id)
        resource = Reading(
            device=device,
            timestamp=datetime.fromisoformat(datetime.now().isoformat(timespec="seconds")),
            temperature=body.temperature,
            humidity=body.humidity,
        )
        flush()
        constants.cache[device.id] = resource.to_model()

        return resource.to_model()


@router.get(path="/current")
def current_readings(*, device_id: int) -> ReadingModel:
    with db_session:
        device = get_device(device_id=device_id)
        if not device.readings:
            return ReadingModel(
                id=-1,
                timestamp=datetime.fromtimestamp(1),
                temperature=-1,
                humidity=-1,
            )
        if device.id in constants.cache:
            return constants.cache[device.id]
        reading = sorted(device.readings, key=lambda x: x.timestamp)[-1].to_model()
        constants.cache[device.id] = reading
        return reading


@router.get(path="/yearly")
def yearly_readings(*, device_id: int) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_yearly_high_readings(entries=device.readings),
            averages=get_yearly_avg_readings(entries=device.readings),
            lows=get_yearly_low_readings(entries=device.readings),
        )


@router.get(path="/monthly")
def monthly_readings(*, device_id: int, year: int | None = None) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_monthly_high_readings(entries=device.readings, year=year),
            averages=get_monthly_avg_readings(entries=device.readings, year=year),
            lows=get_monthly_low_readings(entries=device.readings, year=year),
        )


@router.get(path="/daily")
def daily_readings(*, device_id: int, year: int | None = None, month: int | None = None) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_daily_high_readings(entries=device.readings, year=year, month=month),
            averages=get_daily_avg_readings(entries=device.readings, year=year, month=month),
            lows=get_daily_low_readings(entries=device.readings, year=year, month=month),
        )


@router.get(path="/hourly")
def hourly_readings(
    *,
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> Summary:
    with db_session:
        device = get_device(device_id=device_id)
        return Summary(
            highs=get_hourly_high_readings(
                entries=device.readings,
                year=year,
                month=month,
                day=day,
            ),
            averages=get_hourly_avg_readings(
                entries=device.readings,
                year=year,
                month=month,
                day=day,
            ),
            lows=get_hourly_low_readings(entries=device.readings, year=year, month=month, day=day),
        )
