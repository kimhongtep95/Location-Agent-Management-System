from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.agent import Agent
from app.infrastructure.db.models import AgentModel


class SqlAlchemyAgentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, agent: Agent) -> Agent:
        model = AgentModel(
            id=agent.id,
            full_name=agent.full_name,
            email=agent.email,
            phone=agent.phone,
            region=agent.region,
            status=agent.status,
            created_at=agent.created_at,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, agent_id: UUID) -> Agent | None:
        model = await self._session.get(AgentModel, agent_id)
        return self._to_domain(model) if model else None

    async def update(self, agent: Agent) -> Agent:
        model = await self._session.get(AgentModel, agent.id)
        if model is None:
            raise ValueError("Agent not found for update.")
        model.full_name = agent.full_name
        model.email = agent.email
        model.phone = agent.phone
        model.region = agent.region
        model.status = agent.status
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def delete(self, agent_id: UUID) -> None:
        model = await self._session.get(AgentModel, agent_id)
        if model is None:
            return
        await self._session.delete(model)
        await self._session.commit()

    async def list(
        self, status: str | None = None, region: str | None = None
    ) -> list[Agent]:
        stmt = select(AgentModel)
        if status:
            stmt = stmt.where(AgentModel.status == status)
        if region:
            stmt = stmt.where(AgentModel.region == region)
        stmt = stmt.order_by(AgentModel.created_at.desc())
        result = await self._session.execute(stmt)
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: AgentModel) -> Agent:
        return Agent(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            phone=model.phone,
            region=model.region,
            status=model.status,
            created_at=model.created_at,
        )
