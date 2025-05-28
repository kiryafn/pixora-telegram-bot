from bot.models.job_listing import JobListing
from bot.services.job_listing_service import job_listing_service
from bot.services.listing_preference_service import listing_preference_service
from bot.core import logger


class JobListingServicePipeline:
    async def process_item(self, item, spider):
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