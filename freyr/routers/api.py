__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter, Body
from pony.orm import db_session

from freyr.database.tables import Device, Reading
from freyr.models import DeviceModel, LatestDeviceModel, NewReading, ReadingModel
from freyr.responses import ErrorResponse

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
reading_router = APIRouter(prefix="/readings", tags=["Reading"])


@reading_router.post(path="", status_code=204)
def add_reading(reading: NewReading) -> None:
    with db_session:
        device = Device.get(name=reading.device)
        if not device:
            device = Device(name=reading.device)
        Reading(
            device=device,
            timestamp=datetime.fromisoformat(datetime.now().isoformat(timespec="seconds")),
            temperature=reading.temperature,
            humidity=reading.humidity,
        )


@reading_router.post(path="/error", status_code=204)
def device_error(error: str = Body(embed=True)) -> None:
    LOGGER.error(error)


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
def current_readings(name: str | None = None) -> list[LatestDeviceModel]:
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
def yearly_readings() -> list[DeviceModel]:
    def to_yearly(readings: list[Reading]) -> list[ReadingModel]:
        yearly = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0, day=1, month=1)
            if key not in yearly:
                yearly[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > yearly[key].temperature:
                yearly[key].temperature = entry.temperature
            if entry.humidity > yearly[key].humidity:
                yearly[key].humidity = entry.humidity
        return sorted(yearly.values(), reverse=True)

    with db_session:
        devices = Device.select()
        return sorted(
            {DeviceModel(name=x.name, readings=to_yearly(readings=x.readings)) for x in devices},
        )


@reading_router.get(path="/monthly")
def monthly_readings(year: int = 0) -> list[DeviceModel]:
    def to_monthly(readings: list[Reading], year: int = 0) -> list[ReadingModel]:
        monthly = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0, day=1)
            if year and key.year != year:
                continue
            if key not in monthly:
                monthly[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > monthly[key].temperature:
                monthly[key].temperature = entry.temperature
            if entry.humidity > monthly[key].humidity:
                monthly[key].humidity = entry.humidity
        return sorted(monthly.values(), reverse=True)

    with db_session:
        devices = Device.select()
        return sorted(
            {
                DeviceModel(
                    name=x.name,
                    readings=to_monthly(readings=x.readings, year=year),
                )
                for x in devices
            },
        )


@reading_router.get(path="/daily")
def daily_readings(year: int = 0, month: int = 0) -> list[DeviceModel]:
    def to_daily(readings: list[Reading], year: int = 0, month: int = 0) -> list[ReadingModel]:
        daily = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0, hour=0)
            if year and key.year != year:
                continue
            if month and key.month != month:
                continue
            if key not in daily:
                daily[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > daily[key].temperature:
                daily[key].temperature = entry.temperature
            if entry.humidity > daily[key].humidity:
                daily[key].humidity = entry.humidity
        return sorted(daily.values(), reverse=True)

    with db_session:
        devices = Device.select()
        return sorted(
            {
                DeviceModel(
                    name=x.name,
                    readings=to_daily(readings=x.readings, year=year, month=month),
                )
                for x in devices
            },
        )


@reading_router.get(path="/hourly")
def hourly_readings(year: int = 0, month: int = 0, day: int = 0) -> list[DeviceModel]:
    def to_hourly(
        readings: list[Reading],
        year: int = 0,
        month: int = 0,
        day: int = 0,
    ) -> list[ReadingModel]:
        hourly = {}
        for entry in sorted(readings, key=lambda x: x.timestamp, reverse=True):
            timestamp = datetime.fromisoformat(entry.timestamp.isoformat(timespec="seconds"))
            key = timestamp.replace(second=0, minute=0)
            if year and key.year != year:
                continue
            if month and key.month != month:
                continue
            if day and key.day != day:
                continue
            if key not in hourly:
                hourly[key] = ReadingModel(
                    timestamp=key,
                    temperature=entry.temperature,
                    humidity=entry.humidity,
                )
            if entry.temperature > hourly[key].temperature:
                hourly[key].temperature = entry.temperature
            if entry.humidity > hourly[key].humidity:
                hourly[key].humidity = entry.humidity
        return sorted(hourly.values(), reverse=True)

    with db_session:
        devices = Device.select()
        return sorted(
            {
                DeviceModel(
                    name=x.name,
                    readings=to_hourly(readings=x.readings, year=year, month=month, day=day),
                )
                for x in devices
            },
        )


router.include_router(reading_router)
