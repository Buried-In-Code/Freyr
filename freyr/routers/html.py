__all__ = ["router"]

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from freyr import get_project
from freyr.database import get_session
from freyr.models import Device

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project() / "templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(*, request: Request, session: Session = Depends(get_session)) -> Response:
    devices = session.exec(select(Device)).all()
    return templates.TemplateResponse(
        name="dashboard.html.jinja", context={"request": request, "devices": sorted(devices)}
    )


@router.get(path="/{device_id}", response_class=HTMLResponse)
def get_device(
    *,
    request: Request,
    session: Session = Depends(get_session),
    device_id: int,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> Response:
    devices = session.exec(select(Device)).all()
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    return templates.TemplateResponse(
        name="device.html.jinja",
        context={
            "request": request,
            "devices": sorted(devices),
            "resource": device,
            "options": {
                "years": sorted({x.timestamp.year for x in device.readings}),
                "months": sorted(
                    {x.timestamp.month for x in device.readings if x.timestamp.year == year}
                )
                if year
                else [],
                "days": sorted(
                    {
                        x.timestamp.day
                        for x in device.readings
                        if x.timestamp.year == year and x.timestamp.month == month
                    }
                )
                if year and month
                else [],
            },
            "selected": {"year": year, "month": month, "day": day},
        },
    )
