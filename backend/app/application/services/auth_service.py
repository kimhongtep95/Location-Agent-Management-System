from __future__ import annotations

from uuid import UUID

from app.application.dtos.auth import AuthenticatedUserResponse, TokenResponse
from app.core.exceptions import AuthenticationError, EntityNotFoundError, ValidationError
from app.core.security import JwtTokenService, PasswordHasher
from app.domain.entities.common import Role
from app.domain.entities.user import User
from app.domain.repositories.protocols import UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: JwtTokenService,
    ) -> None:
        self._users = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def register(
        self, email: str, password: str, full_name: str, role: str
    ) -> AuthenticatedUserResponse:
        existing = await self._users.get_by_email(email)
        if existing is not None:
            raise ValidationError("A user with this email already exists.")

        user = User(
            email=email,
            password_hash=self._password_hasher.hash_password(password),
            full_name=full_name,
            role=Role(role),
        )
        created = await self._users.create(user)
        return AuthenticatedUserResponse(
            id=str(created.id),
            email=created.email,
            full_name=created.full_name,
            role=created.role.value,
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self._users.get_by_email(email)
        if user is None or not self._password_hasher.verify_password(
            password, user.password_hash
        ):
            raise AuthenticationError("Invalid email or password.")

        return TokenResponse(
            access_token=self._token_service.create_access_token(
                str(user.id), user.role.value
            )
        )

    async def get_current_user(self, user_id: UUID) -> AuthenticatedUserResponse:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundError("User not found.")
        return AuthenticatedUserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
        )
