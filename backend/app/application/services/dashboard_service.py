from __future__ import annotations

from collections import defaultdict

from app.domain.entities.common import AssignmentStatus
from app.domain.repositories.protocols import (
    AgentRepository,
    AssignmentRepository,
    LocationRepository,
)


class DashboardService:
    def __init__(
        self,
        agent_repository: AgentRepository,
        location_repository: LocationRepository,
        assignment_repository: AssignmentRepository,
    ) -> None:
        self._agents = agent_repository
        self._locations = location_repository
        self._assignments = assignment_repository

    async def get_stats(self) -> dict:
        agents = await self._agents.list()
        locations = await self._locations.list()
        assignments = await self._assignments.list()

        agents_by_status: dict[str, int] = defaultdict(int)
        for agent in agents:
            agents_by_status[agent.status.value] += 1

        active_states = {AssignmentStatus.ASSIGNED, AssignmentStatus.CHECKED_IN}
        active_assignments = sum(1 for a in assignments if a.status in active_states)
        checked_in_now = sum(
            1 for a in assignments if a.status == AssignmentStatus.CHECKED_IN
        )

        counts_by_location: dict[str, int] = defaultdict(int)
        for assignment in assignments:
            counts_by_location[str(assignment.location_id)] += 1

        location_names = {str(loc.id): loc.name for loc in locations}
        assignments_by_location = [
            {
                "location_id": location_id,
                "location_name": location_names.get(location_id, "Unknown"),
                "count": count,
            }
            for location_id, count in counts_by_location.items()
        ]

        return {
            "total_agents": len(agents),
            "agents_by_status": dict(agents_by_status),
            "total_locations": len(locations),
            "active_assignments": active_assignments,
            "checked_in_now": checked_in_now,
            "assignments_by_location": assignments_by_location,
        }
