from __future__ import annotations

from uuid import uuid4

import pytest

from app.application.services.location_service import LocationService
from app.core.exceptions import EntityNotFoundError


async def test_create_and_get_location(location_repository) -> None:
    service = LocationService(location_repository=location_repository)
    location = await service.create_location(
        name="Depot", address="Rd 1", city="Phnom Penh", latitude=11.5, longitude=104.9
    )
    fetched = await service.get_location(location.id)
    assert fetched.name == "Depot"


async def test_list_locations_filters_by_active(location_repository) -> None:
    service = LocationService(location_repository=location_repository)
    await service.create_location(
        name="Open", address="a", city="C", latitude=1.0, longitude=2.0, is_active=True
    )
    await service.create_location(
        name="Closed", address="b", city="C", latitude=1.0, longitude=2.0, is_active=False
    )
    active = await service.list_locations(is_active=True)
    assert [loc.name for loc in active] == ["Open"]


async def test_update_and_delete_location(location_repository) -> None:
    service = LocationService(location_repository=location_repository)
    location = await service.create_location(
        name="Old", address="a", city="C", latitude=1.0, longitude=2.0
    )
    updated = await service.update_location(location.id, name="New", is_active=False)
    assert updated.name == "New"
    assert updated.is_active is False

    await service.delete_location(location.id)
    with pytest.raises(EntityNotFoundError):
        await service.get_location(location.id)


async def test_get_missing_location_raises(location_repository) -> None:
    service = LocationService(location_repository=location_repository)
    with pytest.raises(EntityNotFoundError):
        await service.get_location(uuid4())
