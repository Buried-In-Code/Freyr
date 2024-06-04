__all__ = [
    "get_hourly_low_readings",
    "get_hourly_average_readings",
    "get_hourly_high_readings",
    "get_daily_low_readings",
    "get_daily_average_readings",
    "get_daily_high_readings",
    "get_monthly_low_readings",
    "get_monthly_average_readings",
    "get_monthly_high_readings",
    "get_yearly_low_readings",
    "get_yearly_average_readings",
    "get_yearly_high_readings",
]

from collections.abc import Callable
from datetime import datetime

from freyr.models import Reading, Summary


def filter_readings(
    readings: list[Summary.Reading],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[Summary.Reading]:
    if year:
        readings = [x for x in readings if x.timestamp.year == year]
    if month:
        readings = [x for x in readings if x.timestamp.month == month]
    if day:
        readings = [x for x in readings if x.timestamp.day == day]
    return sorted(readings)


def aggregate_readings(
    readings: list[Reading],
    grouping: Callable[[datetime], datetime],
    aggregation: Callable[[datetime, list[Reading]], Summary.Reading],
) -> list[Summary.Reading]:
    grouped = {}
    for entry in readings:
        key = grouping(entry.timestamp)
        grouped.setdefault(key, []).append(entry)
    return [aggregation(key, values) for key, values in grouped.items()]


def hour_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0)


def day_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0)


def month_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0, day=1)


def year_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0, day=1, month=1)


def high_aggregation(key: datetime, values: list[Reading]) -> Summary.Reading:
    temperature = max((x.temperature for x in values if x.temperature is not None), default=None)
    humidity = max((x.humidity for x in values if x.humidity is not None), default=None)
    return Summary.Reading(timestamp=key, temperature=temperature, humidity=humidity)


def average_aggregation(key: datetime, values: list[Reading]) -> Summary.Reading:
    temperatures = [x.temperature for x in values if x.temperature is not None]
    temperature = round(sum(temperatures) / len(temperatures), 2) if temperatures else None
    humidities = [x.humidity for x in values if x.humidity is not None]
    humidity = round(sum(humidities) / len(humidities), 2) if humidities else None
    return Summary.Reading(timestamp=key, temperature=temperature, humidity=humidity)


def low_aggregation(key: datetime, values: list[Reading]) -> Summary.Reading:
    temperature = min((x.temperature for x in values if x.temperature is not None), default=None)
    humidity = min((x.humidity for x in values if x.humidity is not None), default=None)
    return Summary.Reading(timestamp=key, temperature=temperature, humidity=humidity)


def get_readings(
    readings: list[Reading],
    grouping: Callable[[datetime], datetime],
    aggregation: Callable[[datetime, list[Reading]], Summary.Reading],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[Summary.Reading]:
    aggregated = aggregate_readings(readings=readings, grouping=grouping, aggregation=aggregation)
    return filter_readings(readings=aggregated, year=year, month=month, day=day)


def get_hourly_high_readings(
    readings: list[Reading],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=hour_grouping,
        aggregation=high_aggregation,
        year=year,
        month=month,
        day=day,
    )


def get_hourly_average_readings(
    readings: list[Reading],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=hour_grouping,
        aggregation=average_aggregation,
        year=year,
        month=month,
        day=day,
    )


def get_hourly_low_readings(
    readings: list[Reading],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=hour_grouping,
        aggregation=low_aggregation,
        year=year,
        month=month,
        day=day,
    )


def get_daily_high_readings(
    readings: list[Reading], year: int | None = None, month: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=day_grouping,
        aggregation=high_aggregation,
        year=year,
        month=month,
    )


def get_daily_average_readings(
    readings: list[Reading], year: int | None = None, month: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=day_grouping,
        aggregation=average_aggregation,
        year=year,
        month=month,
    )


def get_daily_low_readings(
    readings: list[Reading], year: int | None = None, month: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings,
        grouping=day_grouping,
        aggregation=low_aggregation,
        year=year,
        month=month,
    )


def get_monthly_high_readings(
    readings: list[Reading], year: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings, grouping=month_grouping, aggregation=high_aggregation, year=year
    )


def get_monthly_average_readings(
    readings: list[Reading], year: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings, grouping=month_grouping, aggregation=average_aggregation, year=year
    )


def get_monthly_low_readings(
    readings: list[Reading], year: int | None = None
) -> list[Summary.Reading]:
    return get_readings(
        readings=readings, grouping=month_grouping, aggregation=low_aggregation, year=year
    )


def get_yearly_high_readings(readings: list[Reading]) -> list[Summary.Reading]:
    return get_readings(readings=readings, grouping=year_grouping, aggregation=high_aggregation)


def get_yearly_average_readings(readings: list[Reading]) -> list[Summary.Reading]:
    return get_readings(readings=readings, grouping=year_grouping, aggregation=average_aggregation)


def get_yearly_low_readings(readings: list[Reading]) -> list[Summary.Reading]:
    return get_readings(readings=readings, grouping=year_grouping, aggregation=low_aggregation)
