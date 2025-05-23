from bot.models.city import City
from bot.repositories.city_repository import CityRepository, city_repository
from bot.services import BaseService


class CityService(BaseService[City]):
    def __init__(self, repository: CityRepository) -> None:
        super().__init__(repository)

    async def get_cities_by_country(self, country_name: str, session=None):
        return await city_repository.get_cities_by_country(country_name, session)

    async def get_city_by_name_and_country(self, city_name: str, country_name: str, session=None):
        return await city_repository.get_city_by_name_and_country(city_name, country_name, session)


city_service = CityService(city_repository)