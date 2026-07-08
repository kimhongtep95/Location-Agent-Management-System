from __future__ import annotations

import pytest

from app.application.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError, ValidationError
from app.core.security import JwtTokenService, PasswordHasher
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


def _service(
    user_repository: SqlAlchemyUserRepository,
    password_hasher: PasswordHasher,
    token_service: JwtTokenService,
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )


async def test_register_creates_user(
    user_repository, password_hasher, token_service
) -> None:
    service = _service(user_repository, password_hasher, token_service)
    created = await service.register(
        email="new@lams.local",
        password="Password123!",
        full_name="New User",
        role="manager",
    )
    assert created.email == "new@lams.local"
    assert created.role == "manager"


async def test_register_duplicate_email_rejected(
    user_repository, password_hasher, token_service
) -> None:
    service = _service(user_repository, password_hasher, token_service)
    await service.register(
        email="dup@lams.local", password="Password123!", full_name="A", role="agent"
    )
    with pytest.raises(ValidationError):
        await service.register(
            email="dup@lams.local", password="Password123!", full_name="B", role="agent"
        )


async def test_login_success_returns_token(
    user_repository, password_hasher, token_service
) -> None:
    service = _service(user_repository, password_hasher, token_service)
    await service.register(
        email="login@lams.local",
        password="Password123!",
        full_name="Login User",
        role="admin",
    )
    token = await service.login(email="login@lams.local", password="Password123!")
    assert token.access_token
    decoded = token_service.decode_access_token(token.access_token)
    assert decoded["role"] == "admin"


async def test_login_wrong_password_rejected(
    user_repository, password_hasher, token_service
) -> None:
    service = _service(user_repository, password_hasher, token_service)
    await service.register(
        email="wrong@lams.local",
        password="Password123!",
        full_name="Wrong User",
        role="agent",
    )
    with pytest.raises(AuthenticationError):
        await service.login(email="wrong@lams.local", password="nope")
