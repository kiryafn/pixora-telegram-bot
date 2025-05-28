from sqlalchemy import select

from bot.configuration.database import async_session
from bot.models import JobPreference, City
from bot.models import Country
from bot.repositories import BaseRepository


class CountryRepository(BaseRepository[Country]):
    """
    Repository for managing Country entities.

    Extends BaseRepository to provide custom logic for retrieving a country
    based on a job preference's ID.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the Country model.
        """
        super().__init__(Country)

    async def get_by_preference_id(self, preference_id: int) -> Country | None:
        """
        Retrieves the country associated with a given job preference ID.

        The lookup is performed by joining the country → city → job preference relationship chain.

        Args:
            preference_id (int): ID of the job preference to look up.

        Returns:
            Country | None: The matching country if found, otherwise None.
        """
        async with async_session() as session:
            stmt = (
                select(Country)
                .join(Country.cities)
                .join(City.job_preferences)
                .where(JobPreference.id == preference_id)
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()


# Singleton instance for accessing country data
country_repository = CountryRepository()