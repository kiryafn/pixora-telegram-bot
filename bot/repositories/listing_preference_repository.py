from typing import Sequence

from sqlalchemy import select

from bot.configuration.database import async_session
from bot.models import ListingPreference, JobListing
from bot.repositories import BaseRepository


class ListingPreferenceRepository(BaseRepository[ListingPreference]):
    def __init__(self) -> None:
        super().__init__(ListingPreference)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(ListingPreference.job_preference_id == preference_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_all_by_listing_id(self, job_id: int) -> Sequence[ListingPreference]:
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(ListingPreference.job_listing_id == job_id)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_all_unseen_by_preference_id(self, preference_id: int) -> Sequence[ListingPreference]:
        async with async_session() as session:
            stmt = (
                select(ListingPreference)
                .where(
                    ListingPreference.job_preference_id == preference_id,
                    ListingPreference.is_seen == False
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()


listing_preference_repository = ListingPreferenceRepository()
