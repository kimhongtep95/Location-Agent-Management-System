from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.application.services.assignment_service import AssignmentService
from app.core.dependencies import CurrentUser, get_assignment_service, get_current_user
from app.presentation.api.v1.schemas import (
    AssignmentResponse,
    CreateAssignmentRequest,
    assignment_to_response,
)

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("", response_model=list[AssignmentResponse])
async def list_assignments(
    agent_id: UUID | None = Query(default=None),
    location_id: UUID | None = Query(default=None),
    status: str | None = Query(default=None),
    _: CurrentUser = Depends(get_current_user),
    service: AssignmentService = Depends(get_assignment_service),
) -> list[AssignmentResponse]:
    assignments = await service.list_assignments(
        agent_id=agent_id, location_id=location_id, status=status
    )
    return [assignment_to_response(assignment) for assignment in assignments]


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    payload: CreateAssignmentRequest,
    _: CurrentUser = Depends(get_current_user),
    service: AssignmentService = Depends(get_assignment_service),
) -> AssignmentResponse:
    assignment = await service.create_assignment(
        agent_id=UUID(payload.agent_id),
        location_id=UUID(payload.location_id),
        notes=payload.notes,
    )
    return assignment_to_response(assignment)


@router.post("/{assignment_id}/check-in", response_model=AssignmentResponse)
async def check_in(
    assignment_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: AssignmentService = Depends(get_assignment_service),
) -> AssignmentResponse:
    assignment = await service.check_in(assignment_id)
    return assignment_to_response(assignment)


@router.post("/{assignment_id}/check-out", response_model=AssignmentResponse)
async def check_out(
    assignment_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: AssignmentService = Depends(get_assignment_service),
) -> AssignmentResponse:
    assignment = await service.check_out(assignment_id)
    return assignment_to_response(assignment)
