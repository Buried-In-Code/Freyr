from __future__ import annotations

__all__ = ["router"]

import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Body
from pony.orm import db_session

from freyr.database.tables import Device, Reading
from freyr.models import DeviceModel, LatestModel, NewReading, ReadingModel, SummaryModel
from freyr.responses import ErrorResponse

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
reading_router = APIRouter(prefix="/readings", tags=["Reading"])


@reading_router.post(path="", status_code=204)
def add_reading(reading: NewReading):  # noqa: ANN202
    with db_session:
        device = Device.get(name=reading.device)
        if not device:
            device = Device(name=reading.device)
        Reading(
            device=device,
            timestamp=datetime.fromisoformat(
                datetime.now(tz=timezone.utc).astimezone().isoformat(timespec="seconds"),
            ),
            temperature=reading.temperature,
            humidity=reading.humidity,
        )


@reading_router.post(path="/error", status_code=204)
def device_error(  # noqa: ANN202
    device: str = Body(embed=True, default="Unknown"),
    error: str = Body(embed=True),
):
    LOGGER.error("%s - %s", device, error)


@reading_router.get(path="")
def list_readings(name: Optional[str] = None) -> list[DeviceModel]:  # noqa: UP007
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
def current_readings(name: Optional[str] = None) -> list[LatestModel]:  # noqa: UP007
    with db_session:
        devices = Device.select()
        if name:
            devices = [
                x
                for x in devices
                if x.name.casefold() in name.casefold() or name.casefold() in x.name.casefold()
            ]
        return sorted({x.to_latest() for x in devices})


@reading_router.get(path="/yearly")
def yearly_readings() -> list[SummaryModel]:
    def to_yearly(readings: list[Reading]) -> tuple[list[ReadingModel], list[ReadingModel]]:
        highs = {}
        lows = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0, day=1, month=1)
            if key not in highs:
                highs[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > highs[key].temperature:
                highs[key].temperature = entry.temperature
            if entry.humidity > highs[key].humidity:
                highs[key].humidity = entry.humidity
            if key not in lows:
                lows[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature < lows[key].temperature:
                lows[key].temperature = entry.temperature
            if entry.humidity < lows[key].humidity:
                lows[key].humidity = entry.humidity
        return sorted(highs.values()), sorted(lows.values())

    with db_session:
        output = set()
        for device in Device.select():
            highs, lows = to_yearly(readings=device.readings)
            output.add(SummaryModel(name=device.name, highs=highs, lows=lows))
        return sorted(output)


@reading_router.get(path="/monthly")
def monthly_readings(year: int = 0) -> list[SummaryModel]:
    def to_monthly(
        readings: list[Reading],
        year: int = 0,
    ) -> tuple[list[ReadingModel], list[ReadingModel]]:
        highs = {}
        lows = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0, day=1)
            if year and key.year != year:
                continue
            if key not in highs:
                highs[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > highs[key].temperature:
                highs[key].temperature = entry.temperature
            if entry.humidity > highs[key].humidity:
                highs[key].humidity = entry.humidity
            if key not in lows:
                lows[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature < lows[key].temperature:
                lows[key].temperature = entry.temperature
            if entry.humidity < lows[key].humidity:
                lows[key].humidity = entry.humidity
        return sorted(highs.values()), sorted(lows.values())

    with db_session:
        output = set()
        for device in Device.select():
            highs, lows = to_monthly(readings=device.readings, year=year)
            output.add(SummaryModel(name=device.name, highs=highs, lows=lows))
        return sorted(output)


@reading_router.get(path="/daily")
def daily_readings(year: int = 0, month: int = 0) -> list[SummaryModel]:
    def to_daily(
        readings: list[Reading],
        year: int = 0,
        month: int = 0,
    ) -> tuple[list[ReadingModel], list[ReadingModel]]:
        highs = {}
        lows = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0)
            if year and key.year != year:
                continue
            if month and key.month != month:
                continue
            if key not in highs:
                highs[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > highs[key].temperature:
                highs[key].temperature = entry.temperature
            if entry.humidity > highs[key].humidity:
                highs[key].humidity = entry.humidity
            if key not in lows:
                lows[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature < lows[key].temperature:
                lows[key].temperature = entry.temperature
            if entry.humidity < lows[key].humidity:
                lows[key].humidity = entry.humidity
        return sorted(highs.values()), sorted(lows.values())

    with db_session:
        output = set()
        for device in Device.select():
            highs, lows = to_daily(readings=device.readings, year=year, month=month)
            output.add(SummaryModel(name=device.name, highs=highs, lows=lows))
        return sorted(output)


@reading_router.get(path="/hourly")
def hourly_readings(year: int = 0, month: int = 0, day: int = 0) -> list[SummaryModel]:
    def to_hourly(
        readings: list[Reading],
        year: int = 0,
        month: int = 0,
        day: int = 0,
    ) -> tuple[list[ReadingModel], list[ReadingModel]]:
        highs = {}
        lows = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0)
            if year and key.year != year:
                continue
            if month and key.month != month:
                continue
            if day and key.day != day:
                continue
            if key not in highs:
                highs[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > highs[key].temperature:
                highs[key].temperature = entry.temperature
            if entry.humidity > highs[key].humidity:
                highs[key].humidity = entry.humidity
            if key not in lows:
                lows[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature < lows[key].temperature:
                lows[key].temperature = entry.temperature
            if entry.humidity < lows[key].humidity:
                lows[key].humidity = entry.humidity
        return sorted(highs.values()), sorted(lows.values())

    with db_session:
        output = set()
        for device in Device.select():
            highs, lows = to_hourly(readings=device.readings, year=year, month=month, day=day)
            output.add(SummaryModel(name=device.name, highs=highs, lows=lows))
        return sorted(output)


router.include_router(reading_router)
