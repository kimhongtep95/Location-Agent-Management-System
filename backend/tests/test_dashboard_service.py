from __future__ import annotations

from app.application.services.agent_service import AgentService
from app.application.services.assignment_service import AssignmentService
from app.application.services.dashboard_service import DashboardService
from app.application.services.location_service import LocationService


async def test_dashboard_stats(
    assignment_repository, agent_repository, location_repository
) -> None:
    agents = AgentService(agent_repository=agent_repository)
    locations = LocationService(location_repository=location_repository)
    assignments = AssignmentService(
        assignment_repository=assignment_repository,
        agent_repository=agent_repository,
        location_repository=location_repository,
    )

    a1 = await agents.create_agent(
        full_name="A1", email="a1@x", phone="1", region="R", status="active"
    )
    await agents.create_agent(
        full_name="A2", email="a2@x", phone="2", region="R", status="inactive"
    )
    loc = await locations.create_location(
        name="L", address="a", city="C", latitude=1.0, longitude=2.0
    )
    assignment = await assignments.create_assignment(a1.id, loc.id)
    await assignments.check_in(assignment.id)

    stats = await DashboardService(
        agent_repository=agent_repository,
        location_repository=location_repository,
        assignment_repository=assignment_repository,
    ).get_stats()

    assert stats["total_agents"] == 2
    assert stats["agents_by_status"]["active"] == 1
    assert stats["agents_by_status"]["inactive"] == 1
    assert stats["total_locations"] == 1
    assert stats["active_assignments"] == 1
    assert stats["checked_in_now"] == 1
    assert stats["assignments_by_location"][0]["count"] == 1
