from typing import Sequence

from bot.models.job_listing import JobListing
from bot.repositories.job_listing_repository import JobListingRepository, job_listing_repository
from bot.services import BaseService


class JobListingService(BaseService[JobListing]):
    repository: JobListingRepository

    def __init__(self, repository: JobListingRepository) -> None:
        super().__init__(repository)

    async def get_by_job_url(self, url: str) -> JobListing | None:
        return await self.repository.get_by_job_url(url)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[JobListing]:
        return await self.repository.get_all_by_preference_id(preference_id)

    async def mark_all_not_seen(self, preference_id: int) -> None:
        await self.repository.mark_all_not_seen(preference_id)

    async def expire_not_seen(self, preference_id: int, marker: str) -> None:
        await self.repository.expire_not_seen(preference_id, marker)


job_listing_service = JobListingService(job_listing_repository)