from bot.models.city import City
from bot.repositories.city_repository import CityRepository, city_repository
from bot.services import BaseService


class CityService(BaseService[City]):
    def __init__(self, repository: CityRepository) -> None:
        super().__init__(repository)

city_service = CityService(city_repository)