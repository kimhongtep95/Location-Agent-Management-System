from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.assignment import Assignment
from app.infrastructure.db.models import AssignmentModel


class SqlAlchemyAssignmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, assignment: Assignment) -> Assignment:
        model = AssignmentModel(
            id=assignment.id,
            agent_id=assignment.agent_id,
            location_id=assignment.location_id,
            status=assignment.status,
            assigned_at=assignment.assigned_at,
            check_in_at=assignment.check_in_at,
            check_out_at=assignment.check_out_at,
            notes=assignment.notes,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, assignment_id: UUID) -> Assignment | None:
        model = await self._session.get(AssignmentModel, assignment_id)
        return self._to_domain(model) if model else None

    async def update(self, assignment: Assignment) -> Assignment:
        model = await self._session.get(AssignmentModel, assignment.id)
        if model is None:
            raise ValueError("Assignment not found for update.")
        model.status = assignment.status
        model.check_in_at = assignment.check_in_at
        model.check_out_at = assignment.check_out_at
        model.notes = assignment.notes
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def list(
        self,
        agent_id: UUID | None = None,
        location_id: UUID | None = None,
        status: str | None = None,
    ) -> list[Assignment]:
        stmt = select(AssignmentModel)
        if agent_id:
            stmt = stmt.where(AssignmentModel.agent_id == agent_id)
        if location_id:
            stmt = stmt.where(AssignmentModel.location_id == location_id)
        if status:
            stmt = stmt.where(AssignmentModel.status == status)
        stmt = stmt.order_by(AssignmentModel.assigned_at.desc())
        result = await self._session.execute(stmt)
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: AssignmentModel) -> Assignment:
        return Assignment(
            id=model.id,
            agent_id=model.agent_id,
            location_id=model.location_id,
            status=model.status,
            assigned_at=model.assigned_at,
            check_in_at=model.check_in_at,
            check_out_at=model.check_out_at,
            notes=model.notes,
        )
