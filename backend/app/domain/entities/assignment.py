from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.common import AssignmentStatus


@dataclass(slots=True)
class Assignment:
    agent_id: UUID
    location_id: UUID
    status: AssignmentStatus = AssignmentStatus.ASSIGNED
    id: UUID = field(default_factory=uuid4)
    assigned_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    check_in_at: datetime | None = None
    check_out_at: datetime | None = None
    notes: str | None = None
