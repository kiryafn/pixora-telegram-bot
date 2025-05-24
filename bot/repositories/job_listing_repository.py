from sqlalchemy import select, Sequence, update
from bot.core.data import async_session

from bot.models.job_listing import JobListing
from bot.models.job_preference import JobPreference
from bot.repositories import BaseRepository


class JobListingRepository(BaseRepository[JobListing]):
    def __init__(self) -> None:
        super().__init__(JobListing)

    async def get_by_job_url(self, job_url: str) -> JobListing | None:
        async with async_session() as session:
            stmt = (
                select(JobListing)
                .where(JobListing.job_url == job_url)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[JobListing]:
        async with async_session() as session:
            stmt = (
                select(JobListing)
                .join(JobListing.job_preferences)
                .where(JobPreference.id == preference_id)
            )

            result = await session.execute(stmt)
            return result.scalars().all()

    async def mark_all_not_seen(self, preference_id: int) -> None:
        async with async_session() as session:
            stmt = (
                update(JobListing)
                .where(JobListing.job_preferences.any(JobPreference.id == preference_id))
                .values(is_seen=False, seen_marker=None)
            )

            await session.execute(stmt)
            await session.commit()

    async def expire_not_seen(self, preference_id: int, marker: str) -> None:
        async with async_session() as session:
            stmt = (
                update(JobListing)
                .where(
                    JobListing.job_preferences.any(JobPreference.id == preference_id),
                    JobListing.seen_marker != marker
                )
                .values(is_active=False)
            )

            await session.execute(stmt)
            await session.commit()

job_listing_repository = JobListingRepository()