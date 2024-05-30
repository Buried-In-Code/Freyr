__all__ = ["router"]

import logging

from fastapi import APIRouter

from freyr.responses import ErrorResponse
from freyr.routers.api.device import router as device_router

LOGGER = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api", responses={422: {"description": "Validation error", "model": ErrorResponse}}
)
router.include_router(device_router)
