from typing import Sequence

from sqlalchemy import select

from bot.models import City
from bot.repositories import BaseRepository
from bot.configuration.database import async_session


class CityRepository(BaseRepository[City]):
    """
    Repository for managing City entities.

    Provides methods to retrieve cities based on country name and city name,
    in addition to the standard CRUD operations inherited from BaseRepository.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the City model.
        """
        super().__init__(City)

    async def get_all_cities_by_country(self, country_name: str) -> Sequence[City]:
        """
        Retrieves all cities that belong to a given country by name.

        Args:
            country_name (str): The name of the country to filter by.

        Returns:
            Sequence[City]: A list of City instances located in the specified country.
        """
        async with async_session() as sess:
            stmt = (
                select(City)
                .join(City.country)
                .where(City.country.has(name=country_name))
            )

            result = await sess.execute(stmt)
            return result.scalars().all()

    async def get_city_by_name_and_country(self, city_name: str, country_name: str) -> City | None:
        """
        Retrieves a single city by its name and country name.

        Args:
            city_name (str): The name of the city.
            country_name (str): The name of the country the city belongs to.

        Returns:
            City | None: The matching City instance if found, otherwise None.
        """
        async with async_session() as sess:
            stmt = (
                select(City)
                .join(City.country)
                .where(City.name == city_name, City.country.has(name=country_name))
            )

            result = await sess.execute(stmt)
            return result.scalar_one_or_none()


# Singleton instance for accessing city data
city_repository = CityRepository()