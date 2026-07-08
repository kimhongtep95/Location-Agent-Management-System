from __future__ import annotations

from fastapi import APIRouter, Depends

from app.application.services.dashboard_service import DashboardService
from app.core.dependencies import CurrentUser, get_current_user, get_dashboard_service
from app.presentation.api.v1.schemas import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_stats(
    _: CurrentUser = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardStatsResponse:
    payload = await service.get_stats()
    return DashboardStatsResponse.model_validate(payload)
