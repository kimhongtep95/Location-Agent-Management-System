from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.agent_service import AgentService
from app.application.services.assignment_service import AssignmentService
from app.application.services.auth_service import AuthService
from app.application.services.dashboard_service import DashboardService
from app.application.services.location_service import LocationService
from app.core.config import Settings, get_settings
from app.core.security import JwtTokenService, PasswordHasher
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.sqlalchemy_agent_repository import (
    SqlAlchemyAgentRepository,
)
from app.infrastructure.repositories.sqlalchemy_assignment_repository import (
    SqlAlchemyAssignmentRepository,
)
from app.infrastructure.repositories.sqlalchemy_location_repository import (
    SqlAlchemyLocationRepository,
)
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@dataclass(slots=True)
class CurrentUser:
    user_id: UUID
    role: str


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_token_service(settings: Settings = Depends(get_settings)) -> JwtTokenService:
    return JwtTokenService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        access_minutes=settings.access_token_minutes,
    )


def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: JwtTokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(
        user_repository=SqlAlchemyUserRepository(session),
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_agent_service(session: AsyncSession = Depends(get_db_session)) -> AgentService:
    return AgentService(agent_repository=SqlAlchemyAgentRepository(session))


def get_location_service(
    session: AsyncSession = Depends(get_db_session),
) -> LocationService:
    return LocationService(location_repository=SqlAlchemyLocationRepository(session))


def get_assignment_service(
    session: AsyncSession = Depends(get_db_session),
) -> AssignmentService:
    return AssignmentService(
        assignment_repository=SqlAlchemyAssignmentRepository(session),
        agent_repository=SqlAlchemyAgentRepository(session),
        location_repository=SqlAlchemyLocationRepository(session),
    )


def get_dashboard_service(
    session: AsyncSession = Depends(get_db_session),
) -> DashboardService:
    return DashboardService(
        agent_repository=SqlAlchemyAgentRepository(session),
        location_repository=SqlAlchemyLocationRepository(session),
        assignment_repository=SqlAlchemyAssignmentRepository(session),
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: JwtTokenService = Depends(get_token_service),
) -> CurrentUser:
    try:
        payload = token_service.decode_access_token(token)
    except Exception as exc:  # pragma: no cover - framework boundary
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
        ) from exc

    return CurrentUser(user_id=UUID(payload["sub"]), role=payload["role"])
