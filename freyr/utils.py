__all__ = [
    "get_hourly_low_readings",
    "get_hourly_avg_readings",
    "get_hourly_high_readings",
    "get_daily_low_readings",
    "get_daily_avg_readings",
    "get_daily_high_readings",
    "get_monthly_low_readings",
    "get_monthly_avg_readings",
    "get_monthly_high_readings",
    "get_yearly_low_readings",
    "get_yearly_avg_readings",
    "get_yearly_high_readings",
]

from collections.abc import Callable
from datetime import datetime

from freyr.models import ReadingModel


def filter_entries(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[ReadingModel]:
    if year:
        entries = [x for x in entries if x.timestamp.year == year]
    if month:
        entries = [x for x in entries if x.timestamp.month == month]
    if day:
        entries = [x for x in entries if x.timestamp.day == day]
    return entries


def aggregate_entries(
    entries: list[ReadingModel],
    grouping: Callable[[datetime], datetime],
    aggregation: Callable[[datetime, list[ReadingModel]], ReadingModel],
) -> list[ReadingModel]:
    grouped = {}
    for entry in entries:
        key = grouping(entry.timestamp)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)
    return [aggregation(key, values) for key, values in grouped.items()]


def hour_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0)


def day_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0)


def month_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0, day=1)


def year_grouping(value: datetime) -> datetime:
    return value.replace(second=0, minute=0, hour=0, day=1, month=1)


def high_aggregation(key: datetime, values: list[ReadingModel]) -> ReadingModel:
    temperature = max(x.temperature for x in values)
    humidity = max(x.humidity for x in values)
    return ReadingModel(timestamp=key, temperature=temperature, humidity=humidity)


def average_aggregation(key: datetime, values: list[ReadingModel]) -> ReadingModel:
    temperatures = [x.temperature for x in values]
    temperature = round(sum(temperatures) / len(temperatures), 2)
    humidities = [x.humidity for x in values]
    humidity = round(sum(humidities) / len(humidities), 2)
    return ReadingModel(timestamp=key, temperature=temperature, humidity=humidity)


def low_aggregation(key: datetime, values: list[ReadingModel]) -> ReadingModel:
    temperature = min(x.temperature for x in values)
    humidity = min(x.humidity for x in values)
    return ReadingModel(timestamp=key, temperature=temperature, humidity=humidity)


def get_hourly_high_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=hour_grouping,
        aggregation=high_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month, day=day)


def get_hourly_avg_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=hour_grouping,
        aggregation=average_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month, day=day)


def get_hourly_low_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=hour_grouping,
        aggregation=low_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month, day=day)


def get_daily_high_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=day_grouping,
        aggregation=high_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month)


def get_daily_avg_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=day_grouping,
        aggregation=average_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month)


def get_daily_low_readings(
    entries: list[ReadingModel],
    year: int | None = None,
    month: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=day_grouping,
        aggregation=low_aggregation,
    )
    return filter_entries(entries=entries, year=year, month=month)


def get_monthly_high_readings(
    entries: list[ReadingModel],
    year: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=high_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_monthly_avg_readings(
    entries: list[ReadingModel],
    year: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=average_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_monthly_low_readings(
    entries: list[ReadingModel],
    year: int | None = None,
) -> list[ReadingModel]:
    entries = aggregate_entries(
        entries=entries,
        grouping=month_grouping,
        aggregation=low_aggregation,
    )
    return filter_entries(entries=entries, year=year)


def get_yearly_high_readings(entries: list[ReadingModel]) -> list[ReadingModel]:
    return aggregate_entries(entries=entries, grouping=year_grouping, aggregation=high_aggregation)


def get_yearly_avg_readings(entries: list[ReadingModel]) -> list[ReadingModel]:
    return aggregate_entries(
        entries=entries,
        grouping=year_grouping,
        aggregation=average_aggregation,
    )


def get_yearly_low_readings(entries: list[ReadingModel]) -> list[ReadingModel]:
    return aggregate_entries(entries=entries, grouping=year_grouping, aggregation=low_aggregation)
