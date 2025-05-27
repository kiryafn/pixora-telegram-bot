from bot.models import JobPreference
from bot.repositories import CityRepository, city_repository
from bot.repositories import JobPreferenceRepository, job_preference_repository
from bot.repositories import UserRepository, user_repository
from bot.services import BaseService


class JobPreferenceService(BaseService[JobPreference]):
    def __init__(
            self,
            repository: JobPreferenceRepository,
            user_repository: UserRepository,
            city_repository: CityRepository
    ) -> None:
        super().__init__(repository)
        self.user_repository = user_repository
        self.city_repository = city_repository

    async def save(self, job_preference: JobPreference) -> None:
        user = await self.user_repository.get_by_id(job_preference.user_id)
        if not user:
            raise Exception(f"User {job_preference.user_id} not found")

        city = await self.city_repository.get_by_id(job_preference.city_id)
        if not city:
            raise Exception(f"City {job_preference.city_id} not found")

        await self.repository.save(job_preference)

    async def get_preference_by_user_id(self, id: int):
        return await job_preference_repository.get_by_user_id(id)


job_preference_service = JobPreferenceService(job_preference_repository, user_repository, city_repository)
