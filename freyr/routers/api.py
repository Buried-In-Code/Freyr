__all__ = ["router"]

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, desc, select

from freyr.database import get_session
from freyr.models import (
    Device,
    DeviceCreate,
    DevicePublic,
    Reading,
    ReadingCreate,
    ReadingPublic,
    Summary,
)
from freyr.responses import ErrorResponse
from freyr.utils import (
    get_daily_average_readings,
    get_daily_high_readings,
    get_daily_low_readings,
    get_hourly_average_readings,
    get_hourly_high_readings,
    get_hourly_low_readings,
    get_monthly_average_readings,
    get_monthly_high_readings,
    get_monthly_low_readings,
    get_yearly_average_readings,
    get_yearly_high_readings,
    get_yearly_low_readings,
)

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api", responses={422: {"description": "Validation error", "model": ErrorResponse}}
)


@router.get(path="/devices", response_model=list[DevicePublic])
def list_devices(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return session.exec(select(Device).offset(offset).limit(limit)).all()


@router.post(path="/devices", status_code=201, response_model=DevicePublic)
def create_device(*, session: Session = Depends(get_session), device: DeviceCreate):
    db_device = Device.model_validate(device)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device


@router.get(path="/devices/{device_id}", response_model=DevicePublic)
def get_device(*, session: Session = Depends(get_session), device_id: int):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    return device


@router.get(path="/devices/{device_id}/readings", response_model=list[ReadingPublic])
def list_device_readings(
    *,
    session: Session = Depends(get_session),
    device_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return list_readings(session=session, device_id=device_id, offset=offset, limit=limit)


@router.post(path="/devices/{device_id}/readings", status_code=201, response_model=ReadingPublic)
def create_device_reading(
    *, session: Session = Depends(get_session), device_id: int, reading: ReadingCreate
):
    if reading.device_id is None:
        reading.device_id = device_id
    elif reading.device_id != device_id:
        raise HTTPException(status_code=400, detail="Body device_id doesn't match Path device_id")
    return create_reading(session=session, reading=reading)


@router.get(path="/devices/{device_id}/readings/yearly")
def yearly_readings(
    *, session: Session = Depends(get_session), device_id: int, limit: int = 100, offset: int = 0
) -> Summary:
    readings = session.exec(select(Reading).where(Reading.device_id == device_id)).all()
    return Summary(
        highs=get_yearly_high_readings(readings=readings)[offset : offset + limit],
        averages=get_yearly_average_readings(readings=readings)[offset : offset + limit],
        lows=get_yearly_low_readings(readings=readings)[offset : offset + limit],
    )


@router.get(path="/monthly")
def monthly_readings(
    *,
    session: Session = Depends(get_session),
    device_id: int,
    year: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> Summary:
    readings = session.exec(select(Reading).where(Reading.device_id == device_id)).all()
    return Summary(
        highs=get_monthly_high_readings(readings=readings, year=year)[offset : offset + limit],
        averages=get_monthly_average_readings(readings=readings, year=year)[
            offset : offset + limit
        ],
        lows=get_monthly_low_readings(readings=readings, year=year)[offset : offset + limit],
    )


@router.get(path="/daily")
def daily_readings(
    *,
    session: Session = Depends(get_session),
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> Summary:
    readings = session.exec(select(Reading).where(Reading.device_id == device_id)).all()
    return Summary(
        highs=get_daily_high_readings(readings=readings, year=year, month=month)[
            offset : offset + limit
        ],
        averages=get_daily_average_readings(readings=readings, year=year, month=month)[
            offset : offset + limit
        ],
        lows=get_daily_low_readings(readings=readings, year=year, month=month)[
            offset : offset + limit
        ],
    )


@router.get(path="/hourly")
def hourly_readings(
    *,
    session: Session = Depends(get_session),
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> Summary:
    readings = session.exec(select(Reading).where(Reading.device_id == device_id)).all()
    return Summary(
        highs=get_hourly_high_readings(readings=readings, year=year, month=month, day=day)[
            offset : offset + limit
        ],
        averages=get_hourly_average_readings(readings=readings, year=year, month=month, day=day)[
            offset : offset + limit
        ],
        lows=get_hourly_low_readings(readings=readings, year=year, month=month, day=day)[
            offset : offset + limit
        ],
    )


@router.get(path="/readings", response_model=list[ReadingPublic])
def list_readings(
    *,
    session: Session = Depends(get_session),
    device_id: int | None = None,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    if device_id:
        readings = session.exec(
            select(Reading)
            .where(Reading.device_id == device_id)
            .order_by(desc(Reading.timestamp))
            .offset(offset)
            .limit(limit)
        ).all()
    else:
        readings = session.exec(
            select(Reading).order_by(desc(Reading.timestamp)).offset(offset).limit(limit)
        ).all()
    return readings


@router.post(path="/readings", status_code=201, response_model=ReadingPublic)
def create_reading(*, session: Session = Depends(get_session), reading: ReadingCreate):
    if reading.timestamp is None:
        reading.timestamp = datetime.fromisoformat(datetime.now().isoformat(timespec="seconds"))
    db_reading = Reading.model_validate(reading)
    session.add(db_reading)
    session.commit()
    session.refresh(db_reading)
    return db_reading
