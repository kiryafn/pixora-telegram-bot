from sqlalchemy import select, Sequence
from bot.configuration.database import async_session

from bot.models import JobListing
from bot.models import JobPreference
from bot.repositories import BaseRepository


class JobListingRepository(BaseRepository[JobListing]):
    """
    Repository for managing JobListing entities.

    Extends BaseRepository with methods for retrieving listings by job URL
    and job preference associations.
    """

    def __init__(self) -> None:
        """
        Initializes the repository with the JobListing model.
        """
        super().__init__(JobListing)

    async def get_by_job_url(self, job_url: str) -> JobListing | None:
        """
        Retrieves a job listing by its unique URL.

        Args:
            job_url (str): The URL of the job posting.

        Returns:
            JobListing | None: The matching job listing, or None if not found.
        """
        async with async_session() as session:
            stmt = (
                select(JobListing)
                .where(JobListing.job_url == job_url)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[JobListing]:
        """
        Retrieves all job listings associated with a given job preference.

        Args:
            preference_id (int): The ID of the job preference.

        Returns:
            Sequence[JobListing]: A list of job listings matching the preference.
        """
        async with async_session() as session:
            stmt = (
                select(JobListing)
                .join(JobListing.job_preferences)
                .where(JobPreference.id == preference_id)
            )

            result = await session.execute(stmt)
            return result.scalars().all()


# Singleton instance for accessing job listings
job_listing_repository = JobListingRepository()