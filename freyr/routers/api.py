__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter
from pony.orm import db_session

from freyr.constants import constants
from freyr.database.tables import Device, Reading
from freyr.models import DeviceModel, NewReading, SummaryModel
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
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
reading_router = APIRouter(prefix="/readings", tags=["Reading"])


@reading_router.post(path="", status_code=204)
def add_reading(reading: NewReading):  # noqa: ANN202
    with db_session:
        device = Device.get(name=reading.device) or Device(name=reading.device)
        reading = Reading(
            device=device,
            timestamp=datetime.fromisoformat(datetime.now().isoformat(timespec="seconds")),
            temperature=reading.temperature,
            humidity=reading.humidity,
        )
        constants.cache[device.name] = reading.to_model()


@reading_router.get(path="")
def list_readings(name: str | None = None) -> list[DeviceModel]:
    with db_session:
        devices = Device.select()
        if name:
            devices = [
                x
                for x in devices
                if x.name.casefold() in name.casefold() or name.casefold() in x.name.casefold()
            ]
        return sorted({x.to_model() for x in devices})


@reading_router.get(path="/current")
def current_readings(name: str | None = None) -> list[DeviceModel]:
    with db_session:
        devices = Device.select()
        if name:
            devices = [
                x
                for x in devices
                if x.name.casefold() in name.casefold() or name.casefold() in x.name.casefold()
            ]
        output = []
        for device in devices:
            if device.name in constants.cache:
                temp = DeviceModel(name=device.name, readings=[constants.cache[device.name]])
            else:
                reading = sorted(device.readings)[-1].to_model()
                constants.cache[device.name] = reading
                temp = DeviceModel(name=device.name, readings=[reading])
            output.append(temp)
        return sorted(output)


@reading_router.get(path="/yearly")
def yearly_readings() -> list[SummaryModel]:
    with db_session:
        output = set()
        for device in Device.select():
            output.add(
                SummaryModel(
                    name=device.name,
                    highs=get_yearly_high_readings(entries=device.readings),
                    averages=get_yearly_avg_readings(entries=device.readings),
                    lows=get_yearly_low_readings(entries=device.readings),
                ),
            )
        return sorted(output)


@reading_router.get(path="/monthly")
def monthly_readings(*, year: int = 0) -> list[SummaryModel]:
    with db_session:
        output = set()
        for device in Device.select():
            output.add(
                SummaryModel(
                    name=device.name,
                    highs=get_monthly_high_readings(entries=device.readings, year=year),
                    averages=get_monthly_avg_readings(entries=device.readings, year=year),
                    lows=get_monthly_low_readings(entries=device.readings, year=year),
                ),
            )
        return sorted(output)


@reading_router.get(path="/daily")
def daily_readings(*, year: int = 0, month: int = 0) -> list[SummaryModel]:
    with db_session:
        output = set()
        for device in Device.select():
            output.add(
                SummaryModel(
                    name=device.name,
                    highs=get_daily_high_readings(entries=device.readings, year=year, month=month),
                    averages=get_daily_avg_readings(
                        entries=device.readings,
                        year=year,
                        month=month,
                    ),
                    lows=get_daily_low_readings(entries=device.readings, year=year, month=month),
                ),
            )
        return sorted(output)


@reading_router.get(path="/hourly")
def hourly_readings(*, year: int = 0, month: int = 0, day: int = 0) -> list[SummaryModel]:
    with db_session:
        output = set()
        for device in Device.select():
            output.add(
                SummaryModel(
                    name=device.name,
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
                    lows=get_hourly_low_readings(
                        entries=device.readings,
                        year=year,
                        month=month,
                        day=day,
                    ),
                ),
            )
        return sorted(output)


router.include_router(reading_router)
