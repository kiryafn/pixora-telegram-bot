from bot.models.city import City
from bot.repositories import BaseRepository


class CityRepository(BaseRepository[City]):
    def __init__(self) -> None:
        super().__init__(City)

city_repository = CityRepository()