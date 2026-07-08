from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordHasher
from app.domain.entities.common import AgentStatus, AssignmentStatus, Role
from app.infrastructure.db.models import (
    AgentModel,
    AssignmentModel,
    LocationModel,
    UserModel,
)

DEMO_ADMIN_EMAIL = "admin@lams.local"
DEMO_ADMIN_PASSWORD = "Password123!"


async def seed_demo_data(session: AsyncSession) -> None:
    """Insert a demo dataset if the database is empty. Idempotent."""
    existing = await session.scalar(select(func.count()).select_from(UserModel))
    if existing:
        return

    hasher = PasswordHasher()
    session.add(
        UserModel(
            email=DEMO_ADMIN_EMAIL,
            password_hash=hasher.hash_password(DEMO_ADMIN_PASSWORD),
            full_name="LAMS Administrator",
            role=Role.ADMIN,
        )
    )

    agents = [
        AgentModel(
            full_name="Sokha Chan",
            email="sokha.chan@lams.local",
            phone="+855 12 345 678",
            region="Phnom Penh",
            status=AgentStatus.ACTIVE,
        ),
        AgentModel(
            full_name="Dara Kim",
            email="dara.kim@lams.local",
            phone="+855 12 987 654",
            region="Siem Reap",
            status=AgentStatus.ACTIVE,
        ),
        AgentModel(
            full_name="Mealea Sok",
            email="mealea.sok@lams.local",
            phone="+855 96 111 222",
            region="Battambang",
            status=AgentStatus.ON_LEAVE,
        ),
        AgentModel(
            full_name="Vibol Pen",
            email="vibol.pen@lams.local",
            phone="+855 70 333 444",
            region="Phnom Penh",
            status=AgentStatus.INACTIVE,
        ),
    ]

    locations = [
        LocationModel(
            name="Central Warehouse",
            address="Street 271, Sen Sok",
            city="Phnom Penh",
            latitude=11.5564,
            longitude=104.9282,
        ),
        LocationModel(
            name="Angkor Branch",
            address="Charles de Gaulle Blvd",
            city="Siem Reap",
            latitude=13.3671,
            longitude=103.8448,
        ),
        LocationModel(
            name="Riverside Kiosk",
            address="Sisowath Quay",
            city="Phnom Penh",
            latitude=11.5700,
            longitude=104.9319,
        ),
        LocationModel(
            name="Battambang Depot",
            address="National Road 5",
            city="Battambang",
            latitude=13.0957,
            longitude=103.2022,
            is_active=False,
        ),
    ]

    session.add_all(agents)
    session.add_all(locations)
    await session.flush()

    now = datetime.now(UTC)
    session.add_all(
        [
            AssignmentModel(
                agent_id=agents[0].id,
                location_id=locations[0].id,
                status=AssignmentStatus.CHECKED_IN,
                check_in_at=now - timedelta(hours=2),
                notes="Morning stock count.",
            ),
            AssignmentModel(
                agent_id=agents[1].id,
                location_id=locations[1].id,
                status=AssignmentStatus.ASSIGNED,
                notes="Site inspection scheduled.",
            ),
            AssignmentModel(
                agent_id=agents[0].id,
                location_id=locations[2].id,
                status=AssignmentStatus.CHECKED_OUT,
                check_in_at=now - timedelta(days=1, hours=3),
                check_out_at=now - timedelta(days=1, hours=1),
                notes="Weekly restock completed.",
            ),
        ]
    )

    await session.commit()
