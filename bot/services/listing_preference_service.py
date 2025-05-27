from typing import Sequence

from bot.models import ListingPreference, JobListing
from bot.repositories import ListingPreferenceRepository, listing_preference_repository
from bot.services import BaseService


class ListingPreferenceService(BaseService):
    repository: ListingPreferenceRepository

    def __init__(self, repository: ListingPreferenceRepository) -> None:
        super().__init__(repository)

    async def link(self, job_listing_id: int, preference_id: int) -> ListingPreference:
        existing = await listing_preference_repository.get_by_job_listing_id(
            job_listing_id, preference_id
        )

        if existing:
            return existing

        new_link = ListingPreference(
            job_listing_id=job_listing_id,
            job_preference_id=preference_id,
            is_seen=False
        )
        return await listing_preference_repository.save(new_link)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        return await self.repository.get_all_by_preference_id(preference_id)

    async def get_all_by_job_id(self, job_id: int) -> Sequence[ListingPreference]:
        return await self.repository.get_all_by_listing_id(job_id)

    async def get_all_unseen_by_preference_id(self, job_id: int) -> Sequence[ListingPreference]:
        return await self.repository.get_all_unseen_by_preference_id(job_id)


listing_preference_service = ListingPreferenceService(listing_preference_repository)
