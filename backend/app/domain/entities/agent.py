from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.common import AgentStatus


@dataclass(slots=True)
class Agent:
    full_name: str
    email: str
    phone: str
    region: str
    status: AgentStatus = AgentStatus.ACTIVE
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
