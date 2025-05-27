from typing import Sequence

from sqlalchemy import select

from bot.models import City
from bot.repositories import BaseRepository
from bot.configuration.database import async_session


class CityRepository(BaseRepository[City]):
    def __init__(self) -> None:
        super().__init__(City)

    async def get_all_cities_by_country(self, country_name: str) -> Sequence[City]:
        async with async_session() as sess:
            stmt = (
                select(City)
                .join(City.country)
                .where(City.country.has(name=country_name))
            )

            result = await sess.execute(stmt)
            return result.scalars().all()

    async def get_city_by_name_and_country(self, city_name: str, country_name: str) -> City | None:
        async with async_session() as sess:
            stmt = (
                select(City)
                .join(City.country)
                .where(City.name == city_name, City.country.has(name=country_name))
            )

            result = await sess.execute(stmt)
            return result.scalar_one_or_none()


city_repository = CityRepository()