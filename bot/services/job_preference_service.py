from bot.models.job_preference import JobPreference
from bot.repositories.job_preference_repository import JobPreferenceRepository, job_preference_repository
from bot.services import BaseService


class JobPreferenceService(BaseService[JobPreference]):
    def __init__(self, repository: JobPreferenceRepository) -> None:
        super().__init__(repository)

    async def get_preference_by_user_id(self, id: int):
        return await job_preference_repository.get_by_user_id(id)

job_preference_service = JobPreferenceService(job_preference_repository)
