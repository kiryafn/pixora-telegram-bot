from bot.models import Country
from bot.repositories import CountryRepository, country_repository
from bot.services import BaseService


class CountryService(BaseService[Country]):
    """
    Service layer for managing Country entities.

    Inherits basic CRUD operations from BaseService. Can be extended with additional
    business logic related to countries (e.g., validation, formatting, statistics).
    """

    def __init__(self, repository: CountryRepository) -> None:
        """
        Initializes the CountryService with the given repository.

        Args:
            repository (CountryRepository): The repository used to access country data.
        """
        super().__init__(repository)


# Singleton instance for accessing country-related logic
country_service = CountryService(country_repository)