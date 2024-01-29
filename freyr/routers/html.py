__all__ = ["router"]

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pony.orm import db_session

from freyr import get_project_root
from freyr.database.tables import Device

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(*, request: Request) -> Response:
    with db_session:
        return templates.TemplateResponse(
            name="dashboard.html.jinja",
            context={
                "request": request,
                "devices": sorted(x for x in Device.select()),
            },
        )


@router.get(path="/{device_id}", response_class=HTMLResponse)
def device(
    *,
    device_id: int,
    request: Request,
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
) -> Response:
    with db_session:
        resource = Device.get(id=device_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Device not found.")
        return templates.TemplateResponse(
            name="device.html.jinja",
            context={
                "request": request,
                "devices": sorted(x for x in Device.select()),
                "resource": resource,
                "options": {
                    "years": sorted({x.timestamp.year for x in resource.readings}),
                    "months": (
                        sorted(
                            {
                                x.timestamp.month
                                for x in resource.readings
                                if x.timestamp.year == year
                            },
                        )
                        if year
                        else []
                    ),
                    "days": (
                        sorted(
                            {
                                x.timestamp.day
                                for x in resource.readings
                                if x.timestamp.year == year and x.timestamp.month == month
                            },
                        )
                        if year and month
                        else []
                    ),
                },
                "selected": {
                    "year": year,
                    "month": month,
                    "day": day,
                },
            },
        )
