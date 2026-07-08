from __future__ import annotations

from uuid import UUID

from app.core.exceptions import EntityNotFoundError
from app.domain.entities.agent import Agent
from app.domain.entities.common import AgentStatus
from app.domain.repositories.protocols import AgentRepository


class AgentService:
    def __init__(self, agent_repository: AgentRepository) -> None:
        self._agents = agent_repository

    async def create_agent(
        self,
        full_name: str,
        email: str,
        phone: str,
        region: str,
        status: str = "active",
    ) -> Agent:
        agent = Agent(
            full_name=full_name,
            email=email,
            phone=phone,
            region=region,
            status=AgentStatus(status),
        )
        return await self._agents.create(agent)

    async def list_agents(
        self, status: str | None = None, region: str | None = None
    ) -> list[Agent]:
        return await self._agents.list(status=status, region=region)

    async def get_agent(self, agent_id: UUID) -> Agent:
        agent = await self._agents.get_by_id(agent_id)
        if agent is None:
            raise EntityNotFoundError("Agent not found.")
        return agent

    async def update_agent(self, agent_id: UUID, **changes: object) -> Agent:
        agent = await self.get_agent(agent_id)
        if "full_name" in changes and changes["full_name"] is not None:
            agent.full_name = str(changes["full_name"])
        if "email" in changes and changes["email"] is not None:
            agent.email = str(changes["email"])
        if "phone" in changes and changes["phone"] is not None:
            agent.phone = str(changes["phone"])
        if "region" in changes and changes["region"] is not None:
            agent.region = str(changes["region"])
        if "status" in changes and changes["status"] is not None:
            agent.status = AgentStatus(str(changes["status"]))
        return await self._agents.update(agent)

    async def delete_agent(self, agent_id: UUID) -> None:
        await self.get_agent(agent_id)
        await self._agents.delete(agent_id)
