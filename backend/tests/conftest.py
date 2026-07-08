from __future__ import annotations

from collections.abc import AsyncIterator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.security import JwtTokenService, PasswordHasher
from app.infrastructure.db.base import Base
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


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with maker() as db_session:
        yield db_session

    await engine.dispose()


@pytest_asyncio.fixture
def user_repository(session: AsyncSession) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


@pytest_asyncio.fixture
def agent_repository(session: AsyncSession) -> SqlAlchemyAgentRepository:
    return SqlAlchemyAgentRepository(session)


@pytest_asyncio.fixture
def location_repository(session: AsyncSession) -> SqlAlchemyLocationRepository:
    return SqlAlchemyLocationRepository(session)


@pytest_asyncio.fixture
def assignment_repository(session: AsyncSession) -> SqlAlchemyAssignmentRepository:
    return SqlAlchemyAssignmentRepository(session)


@pytest_asyncio.fixture
def password_hasher() -> PasswordHasher:
    return PasswordHasher()


@pytest_asyncio.fixture
def token_service() -> JwtTokenService:
    return JwtTokenService(
        secret="test-secret-key-with-plenty-of-length",
        algorithm="HS256",
        access_minutes=60,
    )
