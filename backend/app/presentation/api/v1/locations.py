from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.application.services.location_service import LocationService
from app.core.dependencies import CurrentUser, get_current_user, get_location_service
from app.presentation.api.v1.schemas import (
    CreateLocationRequest,
    LocationResponse,
    UpdateLocationRequest,
    location_to_response,
)

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("", response_model=list[LocationResponse])
async def list_locations(
    is_active: bool | None = Query(default=None),
    city: str | None = Query(default=None),
    _: CurrentUser = Depends(get_current_user),
    service: LocationService = Depends(get_location_service),
) -> list[LocationResponse]:
    locations = await service.list_locations(is_active=is_active, city=city)
    return [location_to_response(location) for location in locations]


@router.post("", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    payload: CreateLocationRequest,
    _: CurrentUser = Depends(get_current_user),
    service: LocationService = Depends(get_location_service),
) -> LocationResponse:
    location = await service.create_location(
        name=payload.name,
        address=payload.address,
        city=payload.city,
        latitude=payload.latitude,
        longitude=payload.longitude,
        is_active=payload.is_active,
    )
    return location_to_response(location)


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: LocationService = Depends(get_location_service),
) -> LocationResponse:
    location = await service.get_location(location_id)
    return location_to_response(location)


@router.patch("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: UUID,
    payload: UpdateLocationRequest,
    _: CurrentUser = Depends(get_current_user),
    service: LocationService = Depends(get_location_service),
) -> LocationResponse:
    location = await service.update_location(
        location_id,
        **payload.model_dump(exclude_unset=True),
    )
    return location_to_response(location)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: LocationService = Depends(get_location_service),
) -> None:
    await service.delete_location(location_id)
