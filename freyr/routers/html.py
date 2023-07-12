__all__ = ["router"]


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pony.orm import db_session

from freyr import get_project_root
from freyr.database.tables import Device

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/", response_class=HTMLResponse)
def current(request: Request) -> Response:
    return templates.TemplateResponse("current.html.jinja", {"request": request})


@router.get("/historical", response_class=HTMLResponse)
def historical(
    request: Request,
    year: int = 0,
    month: int = 0,
    day: int = 0,
) -> Response:
    def year_list() -> list[int]:
        with db_session:
            return sorted({y.timestamp.year for x in Device.select() for y in x.readings})

    def month_list(year: int) -> list[int]:
        with db_session:
            return sorted(
                {
                    y.timestamp.month
                    for x in Device.select()
                    for y in x.readings
                    if y.timestamp.year == year
                },
            )

    def day_list(year: int, month: int) -> list[int]:
        with db_session:
            return sorted(
                {
                    y.timestamp.day
                    for x in Device.select()
                    for y in x.readings
                    if y.timestamp.year == year and y.timestamp.month == month
                },
            )

    def device_list() -> list[str]:
        with db_session:
            return sorted(x.name for x in Device.select())

    return templates.TemplateResponse(
        "historical.html.jinja",
        {
            "request": request,
            "year_list": year_list(),
            "month_list": month_list(year=year) if year else [],
            "day_list": day_list(year=year, month=month) if year and month else [],
            "year": year,
            "month": month,
            "day": day,
            "device_names": device_list(),
        },
    )
