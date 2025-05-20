from bot.models.country import Country
from bot.repositories import BaseRepository


class CountryRepository(BaseRepository[Country]):
    def __init__(self) -> None:
        super().__init__(Country)

countries_repository = CountryRepository()