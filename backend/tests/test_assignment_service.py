from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.agent_service import AgentService
from app.application.services.assignment_service import AssignmentService
from app.application.services.location_service import LocationService
from app.core.exceptions import EntityNotFoundError, ValidationError


async def _agent_and_location(agent_repository, location_repository):
    agent = await AgentService(agent_repository=agent_repository).create_agent(
        full_name="A", email="a@x", phone="1", region="R"
    )
    location = await LocationService(
        location_repository=location_repository
    ).create_location(name="L", address="a", city="C", latitude=1.0, longitude=2.0)
    return agent, location


def _service(assignment_repository, agent_repository, location_repository):
    return AssignmentService(
        assignment_repository=assignment_repository,
        agent_repository=agent_repository,
        location_repository=location_repository,
    )


async def test_create_assignment(
    assignment_repository, agent_repository, location_repository
) -> None:
    agent, location = await _agent_and_location(agent_repository, location_repository)
    service = _service(assignment_repository, agent_repository, location_repository)
    assignment = await service.create_assignment(agent.id, location.id, notes="Go")
    assert assignment.status.value == "assigned"
    assert assignment.notes == "Go"


async def test_create_assignment_missing_agent_raises(
    assignment_repository, agent_repository, location_repository
) -> None:
    _, location = await _agent_and_location(agent_repository, location_repository)
    service = _service(assignment_repository, agent_repository, location_repository)
    with pytest.raises(EntityNotFoundError):
        await service.create_assignment(uuid4(), location.id)


async def test_check_in_then_check_out_flow(
    assignment_repository, agent_repository, location_repository
) -> None:
    agent, location = await _agent_and_location(agent_repository, location_repository)
    service = _service(assignment_repository, agent_repository, location_repository)
    assignment = await service.create_assignment(agent.id, location.id)

    checked_in = await service.check_in(assignment.id)
    assert checked_in.status.value == "checked_in"
    assert checked_in.check_in_at is not None

    checked_out = await service.check_out(assignment.id)
    assert checked_out.status.value == "checked_out"
    assert checked_out.check_out_at is not None


async def test_check_out_before_check_in_rejected(
    assignment_repository, agent_repository, location_repository
) -> None:
    agent, location = await _agent_and_location(agent_repository, location_repository)
    service = _service(assignment_repository, agent_repository, location_repository)
    assignment = await service.create_assignment(agent.id, location.id)
    with pytest.raises(ValidationError):
        await service.check_out(assignment.id)


async def test_double_check_in_rejected(
    assignment_repository, agent_repository, location_repository
) -> None:
    agent, location = await _agent_and_location(agent_repository, location_repository)
    service = _service(assignment_repository, agent_repository, location_repository)
    assignment = await service.create_assignment(agent.id, location.id)
    await service.check_in(assignment.id)
    with pytest.raises(ValidationError):
        await service.check_in(assignment.id)
