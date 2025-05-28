from typing import Sequence

from bot.models import JobListing
from bot.repositories import JobListingRepository, job_listing_repository
from bot.repositories import JobPreferenceRepository, job_preference_repository
from bot.services import BaseService


class JobListingService(BaseService[JobListing]):
    """
    Service layer for managing JobListing entities.

    Provides additional logic for checking duplicates by job URL
    and retrieving listings based on user preferences.

    Attributes:
        job_preference_repository (JobPreferenceRepository): Repository used for preference-based lookups.
    """

    repository: JobListingRepository

    def __init__(
        self,
        repository: JobListingRepository,
        job_preference_repository: JobPreferenceRepository
    ) -> None:
        """
        Initializes the service with the listing and preference repositories.

        Args:
            repository (JobListingRepository): The repository used for job listings.
            job_preference_repository (JobPreferenceRepository): For preference-based logic.
        """
        super().__init__(repository)
        self.job_preference_repository = job_preference_repository

    # TODO: Add full validation before saving job listing.
    async def save(self, job_listing: JobListing) -> JobListing:
        """
        Saves a job listing to the database.

        If a listing with the same URL already exists, skips duplicate handling (currently no-op).

        Args:
            job_listing (JobListing): The job listing instance to save.

        Returns:
            JobListing: The saved job listing.
        """
        existing = await self.repository.get_by_job_url(job_listing.job_url)
        if existing:
            pass  # Duplicate handling logic to be added here
        return await self.repository.save(job_listing)

    async def get_by_job_url(self, url: str) -> JobListing | None:
        """
        Retrieves a job listing by its unique URL.

        Args:
            url (str): The job listing URL.

        Returns:
            JobListing | None: The job listing if found, otherwise None.
        """
        return await self.repository.get_by_job_url(url)

    async def get_all_by_preference_id(self, preference_id: int) -> Sequence[JobListing]:
        """
        Retrieves all job listings associated with a given job preference ID.

        Args:
            preference_id (int): The ID of the job preference.

        Returns:
            Sequence[JobListing]: A list of matching job listings.
        """
        return await self.repository.get_all_by_preference_id(preference_id)


# Singleton instance for accessing job listing logic
job_listing_service = JobListingService(job_listing_repository, job_preference_repository)