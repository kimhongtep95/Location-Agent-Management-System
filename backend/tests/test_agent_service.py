from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.agent_service import AgentService
from app.core.exceptions import EntityNotFoundError


async def test_create_and_get_agent(agent_repository) -> None:
    service = AgentService(agent_repository=agent_repository)
    agent = await service.create_agent(
        full_name="Test Agent",
        email="t@lams.local",
        phone="000",
        region="Phnom Penh",
    )
    fetched = await service.get_agent(agent.id)
    assert fetched.full_name == "Test Agent"


async def test_list_agents_filters_by_status(agent_repository) -> None:
    service = AgentService(agent_repository=agent_repository)
    await service.create_agent(
        full_name="Active", email="a@x", phone="1", region="R", status="active"
    )
    await service.create_agent(
        full_name="Inactive", email="i@x", phone="2", region="R", status="inactive"
    )
    active = await service.list_agents(status="active")
    assert len(active) == 1
    assert active[0].full_name == "Active"


async def test_update_agent(agent_repository) -> None:
    service = AgentService(agent_repository=agent_repository)
    agent = await service.create_agent(
        full_name="Before", email="b@x", phone="1", region="R"
    )
    updated = await service.update_agent(agent.id, full_name="After", status="on_leave")
    assert updated.full_name == "After"
    assert updated.status.value == "on_leave"


async def test_delete_agent(agent_repository) -> None:
    service = AgentService(agent_repository=agent_repository)
    agent = await service.create_agent(
        full_name="Doomed", email="d@x", phone="1", region="R"
    )
    await service.delete_agent(agent.id)
    with pytest.raises(EntityNotFoundError):
        await service.get_agent(agent.id)


async def test_get_missing_agent_raises(agent_repository) -> None:
    service = AgentService(agent_repository=agent_repository)
    with pytest.raises(EntityNotFoundError):
        await service.get_agent(uuid4())
