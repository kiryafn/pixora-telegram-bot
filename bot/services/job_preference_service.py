from bot.models import JobPreference
from bot.repositories import CityRepository, city_repository
from bot.repositories import JobPreferenceRepository, job_preference_repository
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class JobPreferenceService(BaseService[JobPreference]):
    """
    Service layer for managing JobPreference entities.

    Validates related user and city before saving a job preference.
    Provides convenient access to a user's job preference.

    Attributes:
        user_repository (UserRepository): Used to validate user existence.
        city_repository (CityRepository): Used to validate city existence.
    """

    def __init__(
        self,
        repository: JobPreferenceRepository,
        user_repository: UserRepository,
        city_repository: CityRepository
    ) -> None:
        """
        Initializes the service with related repositories.

        Args:
            repository (JobPreferenceRepository): The job preference repository.
            user_repository (UserRepository): For validating user existence.
            city_repository (CityRepository): For validating city existence.
        """
        super().__init__(repository)
        self.user_repository = user_repository
        self.city_repository = city_repository

    async def save(self, job_preference: JobPreference) -> JobPreference:
        """
        Saves a job preference after validating the user and city references.

        Args:
            job_preference (JobPreference): The job preference to be saved.

        Raises:
            Exception: If the referenced user or city does not exist.
            # TODO: Replace generic Exception with custom exceptions.

        Returns:
            JobPreference: The saved job preference.
        """
        user = await self.user_repository.get_by_id(job_preference.user_id)
        if not user:
            raise Exception(f"User {job_preference.user_id} not found")

        city = await self.city_repository.get_by_id(job_preference.city_id)
        if not city:
            raise Exception(f"City {job_preference.city_id} not found")

        return await self.repository.save(job_preference)

    async def get_preference_by_user_id(self, id: int) -> JobPreference | None:
        """
        Retrieves the job preference associated with the given user ID.

        Args:
            id (int): The user's ID.

        Returns:
            JobPreference | None: The preference if it exists, otherwise None.
        """
        return await job_preference_repository.get_by_user_id(id)


# Singleton instance for accessing job preference logic
job_preference_service = JobPreferenceService(job_preference_repository, user_repository, city_repository)