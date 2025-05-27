from bot.models import Country
from bot.repositories import CountryRepository, country_repository
from bot.services import BaseService


class CountryService(BaseService[Country]):
    def __init__(self, repository: CountryRepository) -> None:
        super().__init__(repository)

country_service = CountryService(country_repository)