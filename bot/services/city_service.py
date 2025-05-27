from bot.models.city import City
from bot.repositories import city_repository, country_repository
from bot.repositories.city_repository import CityRepository
from bot.repositories.country_repository import CountryRepository
from bot.services import BaseService

#todo add custom exception
class CityService(BaseService[City]):
    def __init__(self, repository: CityRepository, country_repository: CountryRepository) -> None:
        super().__init__(repository)
        self.country_repository = country_repository

    async def save(self, city: City) -> None:
        country = await self.country_repository.get_by_id(city.country.id)
        if not country:
            raise Exception(f"Could not find country {city.country.name}")

        await self.repository.save(city)

    async def get_all_cities_by_country(self, country_name: str):
        return await city_repository.get_all_cities_by_country(country_name)

    async def get_city_by_name_and_country(self, city_name: str, country_name: str):
        return await city_repository.get_city_by_name_and_country(city_name, country_name)


city_service = CityService(city_repository, country_repository)
