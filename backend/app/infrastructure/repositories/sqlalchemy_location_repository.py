from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.location import Location
from app.infrastructure.db.models import LocationModel


class SqlAlchemyLocationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, location: Location) -> Location:
        model = LocationModel(
            id=location.id,
            name=location.name,
            address=location.address,
            city=location.city,
            latitude=location.latitude,
            longitude=location.longitude,
            is_active=location.is_active,
            created_at=location.created_at,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, location_id: UUID) -> Location | None:
        model = await self._session.get(LocationModel, location_id)
        return self._to_domain(model) if model else None

    async def update(self, location: Location) -> Location:
        model = await self._session.get(LocationModel, location.id)
        if model is None:
            raise ValueError("Location not found for update.")
        model.name = location.name
        model.address = location.address
        model.city = location.city
        model.latitude = location.latitude
        model.longitude = location.longitude
        model.is_active = location.is_active
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def delete(self, location_id: UUID) -> None:
        model = await self._session.get(LocationModel, location_id)
        if model is None:
            return
        await self._session.delete(model)
        await self._session.commit()

    async def list(
        self, is_active: bool | None = None, city: str | None = None
    ) -> list[Location]:
        stmt = select(LocationModel)
        if is_active is not None:
            stmt = stmt.where(LocationModel.is_active == is_active)
        if city:
            stmt = stmt.where(LocationModel.city == city)
        stmt = stmt.order_by(LocationModel.created_at.desc())
        result = await self._session.execute(stmt)
        return [self._to_domain(model) for model in result.scalars().all()]

    @staticmethod
    def _to_domain(model: LocationModel) -> Location:
        return Location(
            id=model.id,
            name=model.name,
            address=model.address,
            city=model.city,
            latitude=model.latitude,
            longitude=model.longitude,
            is_active=model.is_active,
            created_at=model.created_at,
        )
