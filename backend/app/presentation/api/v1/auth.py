from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.application.dtos.auth import (
    AuthenticatedUserResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.application.services.auth_service import AuthService
from app.core.dependencies import CurrentUser, get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthenticatedUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> AuthenticatedUserResponse:
    return await service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return await service.login(email=payload.email, password=payload.password)


@router.get("/me", response_model=AuthenticatedUserResponse)
async def me(
    current_user: CurrentUser = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> AuthenticatedUserResponse:
    return await service.get_current_user(current_user.user_id)
