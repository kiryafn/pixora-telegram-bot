from sqlalchemy import select
from bot.models.city import City
from bot.repositories import BaseRepository
from bot.core.data import async_session


class CityRepository(BaseRepository[City]):
    def __init__(self) -> None:
        super().__init__(City)

    async def get_cities_by_country(self, country_name: str, session=None):
        stmt = select(City).join(City.country).where(City.country.has(name=country_name))

        if session:
            result = await session.execute(stmt)
            return result.scalars().all()

        # Вызываем async_session(), чтобы получить AsyncSession
        async with async_session() as sess:
            result = await sess.execute(stmt)
            return result.scalars().all()

    async def get_city_by_name_and_country(self, city_name: str, country_name: str, session=None):
        stmt = (
            select(City)
            .join(City.country)
            .where(City.name == city_name, City.country.has(name=country_name))
        )

        if session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        async with async_session() as sess:
            result = await sess.execute(stmt)
            return result.scalar_one_or_none()


city_repository = CityRepository()