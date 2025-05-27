from sqlalchemy import select

from bot.core.data import async_session
from bot.models import JobPreference, City
from bot.models.country import Country
from bot.repositories import BaseRepository


class CountryRepository(BaseRepository[Country]):
    def __init__(self) -> None:
        super().__init__(Country)

    async def get_by_preference_id(self, preference_id: int) -> Country | None:
        async with async_session() as session:
            stmt = (
                select(Country)
                .join(Country.cities)
                .join(City.job_preferences)
                .where(JobPreference.id == preference_id)
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()


country_repository = CountryRepository()