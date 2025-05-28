from bot.models.city import City
from bot.repositories import city_repository, country_repository
from bot.repositories import CityRepository
from bot.repositories import CountryRepository
from bot.services import BaseService
from typing import Sequence


# TODO: Replace generic Exception with a custom application exception.
class CityService(BaseService[City]):
    """
    Service layer for managing City entities.

    Extends BaseService and provides additional logic for validating countries
    when saving cities and for retrieving cities by country or name.

    Attributes:
        country_repository (CountryRepository): Repository used for country lookups.
    """

    def __init__(self, repository: CityRepository, country_repository: CountryRepository) -> None:
        """
        Initializes the CityService with its dependencies.

        Args:
            repository (CityRepository): The city repository.
            country_repository (CountryRepository): The country repository used for validation.
        """
        super().__init__(repository)
        self.country_repository = country_repository

    async def save(self, city: City) -> City:
        """
        Saves a city to the database after verifying that its associated country exists.

        Args:
            city (City): The city instance to save.

        Raises:
            Exception: If the associated country does not exist.
            # Consider replacing with a custom exception type in production.

        Returns:
            City: The saved and refreshed city instance.
        """
        country = await self.country_repository.get_by_id(city.country.id)
        if not country:
            raise Exception(f"Could not find country {city.country.name}")
        return await self.repository.save(city)

    async def get_all_cities_by_country(self, country_name: str) -> Sequence[City]:
        """
        Retrieves all cities that belong to the specified country.

        Args:
            country_name (str): The name of the country.

        Returns:
            Sequence[City]: A list of cities in the given country.
        """
        return await city_repository.get_all_cities_by_country(country_name)

    async def get_city_by_name_and_country(self, city_name: str, country_name: str) -> City | None:
        """
        Retrieves a city by its name and the name of its country.

        Args:
            city_name (str): The name of the city.
            country_name (str): The name of the country.

        Returns:
            City | None: The matching city if found, otherwise None.
        """
        return await city_repository.get_city_by_name_and_country(city_name, country_name)


# Singleton instance for accessing city-related logic
city_service = CityService(city_repository, country_repository)