from bot.models.job_listing import JobListing
from bot.repositories.job_listing_repository import JobListingRepository, job_listing_repository
from bot.services import BaseService


class JobListingService(BaseService[JobListing]):
    def __init__(self, repository: JobListingRepository) -> None:
        super().__init__(repository)

job_listing_service = JobListingService(job_listing_repository)