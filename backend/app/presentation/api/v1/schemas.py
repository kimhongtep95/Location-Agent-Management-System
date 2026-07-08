from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.entities.agent import Agent
from app.domain.entities.assignment import Assignment
from app.domain.entities.common import AgentStatus
from app.domain.entities.location import Location


# ---- Agents ----
class CreateAgentRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    region: str
    status: AgentStatus = AgentStatus.ACTIVE


class UpdateAgentRequest(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    region: str | None = None
    status: AgentStatus | None = None


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: str
    phone: str
    region: str
    status: str
    created_at: datetime


def agent_to_response(agent: Agent) -> AgentResponse:
    return AgentResponse(
        id=str(agent.id),
        full_name=agent.full_name,
        email=agent.email,
        phone=agent.phone,
        region=agent.region,
        status=agent.status.value,
        created_at=agent.created_at,
    )


# ---- Locations ----
class CreateLocationRequest(BaseModel):
    name: str
    address: str
    city: str
    latitude: float
    longitude: float
    is_active: bool = True


class UpdateLocationRequest(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None


class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    address: str
    city: str
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime


def location_to_response(location: Location) -> LocationResponse:
    return LocationResponse(
        id=str(location.id),
        name=location.name,
        address=location.address,
        city=location.city,
        latitude=location.latitude,
        longitude=location.longitude,
        is_active=location.is_active,
        created_at=location.created_at,
    )


# ---- Assignments ----
class CreateAssignmentRequest(BaseModel):
    agent_id: str
    location_id: str
    notes: str | None = None


class AssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_id: str
    location_id: str
    status: str
    assigned_at: datetime
    check_in_at: datetime | None
    check_out_at: datetime | None
    notes: str | None


def assignment_to_response(assignment: Assignment) -> AssignmentResponse:
    return AssignmentResponse(
        id=str(assignment.id),
        agent_id=str(assignment.agent_id),
        location_id=str(assignment.location_id),
        status=assignment.status.value,
        assigned_at=assignment.assigned_at,
        check_in_at=assignment.check_in_at,
        check_out_at=assignment.check_out_at,
        notes=assignment.notes,
    )


# ---- Dashboard ----
class AssignmentsByLocation(BaseModel):
    location_id: str
    location_name: str
    count: int


class DashboardStatsResponse(BaseModel):
    total_agents: int
    agents_by_status: dict[str, int]
    total_locations: int
    active_assignments: int
    checked_in_now: int
    assignments_by_location: list[AssignmentsByLocation]
