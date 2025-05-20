from bot.models.job_listing import JobListing
from bot.repositories import BaseRepository


class JobListingRepository(BaseRepository[JobListing]):
    def __init__(self) -> None:
        super().__init__(JobListing)

job_listing_repository = JobListingRepository()