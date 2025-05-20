from bot.models.job_preference import JobPreference
from bot.repositories import BaseRepository


class JobPreferenceRepository(BaseRepository[JobPreference]):
    def __init__(self) -> None:
        super().__init__(JobPreference)

job_preference_repository = JobPreferenceRepository()
