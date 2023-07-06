__all__ = ["router"]

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from freyr import get_project_root

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> Response:
    return templates.TemplateResponse("current.html.jinja", {"request": request})
