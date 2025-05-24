from sqlalchemy import select, Sequence
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

job_listing_repository = JobListingRepository()