from __future__ import annotations

from uuid import UUID

from app.core.exceptions import EntityNotFoundError
from app.domain.entities.location import Location
from app.domain.repositories.protocols import LocationRepository


class LocationService:
    def __init__(self, location_repository: LocationRepository) -> None:
        self._locations = location_repository

    async def create_location(
        self,
        name: str,
        address: str,
        city: str,
        latitude: float,
        longitude: float,
        is_active: bool = True,
    ) -> Location:
        location = Location(
            name=name,
            address=address,
            city=city,
            latitude=latitude,
            longitude=longitude,
            is_active=is_active,
        )
        return await self._locations.create(location)

    async def list_locations(
        self, is_active: bool | None = None, city: str | None = None
    ) -> list[Location]:
        return await self._locations.list(is_active=is_active, city=city)

    async def get_location(self, location_id: UUID) -> Location:
        location = await self._locations.get_by_id(location_id)
        if location is None:
            raise EntityNotFoundError("Location not found.")
        return location

    async def update_location(self, location_id: UUID, **changes: object) -> Location:
        location = await self.get_location(location_id)
        for attr in ("name", "address", "city"):
            if attr in changes and changes[attr] is not None:
                setattr(location, attr, str(changes[attr]))
        if changes.get("latitude") is not None:
            location.latitude = float(changes["latitude"])  # type: ignore[arg-type]
        if changes.get("longitude") is not None:
            location.longitude = float(changes["longitude"])  # type: ignore[arg-type]
        if changes.get("is_active") is not None:
            location.is_active = bool(changes["is_active"])
        return await self._locations.update(location)

    async def delete_location(self, location_id: UUID) -> None:
        await self.get_location(location_id)
        await self._locations.delete(location_id)
