from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from app.core.exceptions import EntityNotFoundError, ValidationError
from app.domain.entities.assignment import Assignment
from app.domain.entities.common import AssignmentStatus
from app.domain.repositories.protocols import (
    AgentRepository,
    AssignmentRepository,
    LocationRepository,
)


class AssignmentService:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        agent_repository: AgentRepository,
        location_repository: LocationRepository,
    ) -> None:
        self._assignments = assignment_repository
        self._agents = agent_repository
        self._locations = location_repository

    async def create_assignment(
        self, agent_id: UUID, location_id: UUID, notes: str | None = None
    ) -> Assignment:
        if await self._agents.get_by_id(agent_id) is None:
            raise EntityNotFoundError("Agent not found.")
        if await self._locations.get_by_id(location_id) is None:
            raise EntityNotFoundError("Location not found.")

        assignment = Assignment(agent_id=agent_id, location_id=location_id, notes=notes)
        return await self._assignments.create(assignment)

    async def list_assignments(
        self,
        agent_id: UUID | None = None,
        location_id: UUID | None = None,
        status: str | None = None,
    ) -> list[Assignment]:
        return await self._assignments.list(
            agent_id=agent_id, location_id=location_id, status=status
        )

    async def get_assignment(self, assignment_id: UUID) -> Assignment:
        assignment = await self._assignments.get_by_id(assignment_id)
        if assignment is None:
            raise EntityNotFoundError("Assignment not found.")
        return assignment

    async def check_in(self, assignment_id: UUID) -> Assignment:
        assignment = await self.get_assignment(assignment_id)
        if assignment.status != AssignmentStatus.ASSIGNED:
            raise ValidationError("Only an assigned assignment can be checked in.")
        assignment.status = AssignmentStatus.CHECKED_IN
        assignment.check_in_at = datetime.now(UTC)
        return await self._assignments.update(assignment)

    async def check_out(self, assignment_id: UUID) -> Assignment:
        assignment = await self.get_assignment(assignment_id)
        if assignment.status != AssignmentStatus.CHECKED_IN:
            raise ValidationError("Only a checked-in assignment can be checked out.")
        assignment.status = AssignmentStatus.CHECKED_OUT
        assignment.check_out_at = datetime.now(UTC)
        return await self._assignments.update(assignment)
