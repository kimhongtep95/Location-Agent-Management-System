from fastapi import APIRouter

from app.presentation.api.v1.agents import router as agents_router
from app.presentation.api.v1.assignments import router as assignments_router
from app.presentation.api.v1.auth import router as auth_router
from app.presentation.api.v1.dashboard import router as dashboard_router
from app.presentation.api.v1.locations import router as locations_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(agents_router)
api_router.include_router(locations_router)
api_router.include_router(assignments_router)
api_router.include_router(dashboard_router)
