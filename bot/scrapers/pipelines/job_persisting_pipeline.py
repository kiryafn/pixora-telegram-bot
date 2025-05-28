from bot.models.job_listing import JobListing
from bot.services.job_listing_service import job_listing_service
from bot.services.listing_preference_service import listing_preference_service
from bot.core import logger


class JobListingServicePipeline:
    """
    Scrapy pipeline that processes and stores job listing items.

    - Checks if a job listing with the same URL already exists.
    - If it does, links it to a job preference.
    - If not, creates and saves the job listing, then links it.

    Attributes:
        None
    """

    async def process_item(self, item, spider):
        """
        Processes a Scrapy item representing a job listing.

        1. Checks for existing job listing by URL.
        2. If found, links it to the current spider's job preference.
        3. If not found, saves the new job listing and links it.

        Args:
            item (dict): The scraped item from the spider.
            spider: The spider instance that scraped the item. Must have `preference_id`.

        Returns:
            dict: The original item, unchanged.
        """
        url = item.get("url")

        try:
            existing: JobListing | None = await job_listing_service.get_by_job_url(url)
        except Exception as e:
            logger.error(f"❌ Error checking existing record {url}: {e!r}")
            existing = None

        if existing:
            try:
                await listing_preference_service.link(existing.id, spider.preference_id)
            except Exception as e:
                logger.error(f"❌ Error linking existing job to preference: {e!r}")
            return item

        job = JobListing(
            job_title        = item.get("title", ""),
            company_name     = item.get("company", ""),
            company_logo_url = item.get("company_logo_url", ""),
            location         = item.get("location", ""),
            salary           = item.get("salary", ""),
            job_schedule     = item.get("job_schedule", ""),
            job_url          = url,
        )

        try:
            saved: JobListing = await job_listing_service.save(job)
            logger.info(f"✅ Saved job: {saved.job_url}")
        except Exception as e:
            logger.error(f"❌ Error saving job {job.job_url}: {e!r}")
            return item

        try:
            await listing_preference_service.link(saved.id, spider.preference_id)
            logger.info(f"🔗 Linked job_listing {saved.id} with preference {spider.preference_id}")
        except Exception as e:
            logger.error(f"❌ Error linking new job to preference: {e!r}")

        return item