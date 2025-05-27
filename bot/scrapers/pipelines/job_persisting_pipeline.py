from bot.models.job_listing import JobListing
from bot.services.job_listing_service import job_listing_service

from bot.core import logger


class JobListingServicePipeline:
    async def process_item(self, item, spider):
        url = item.get("url")
        try:
            existing: JobListing | None = await job_listing_service.get_by_job_url(url)
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке существующей записи {url}: {e!r}")
            existing = None

        if existing:
            return item

        job = JobListing(
            job_title=item.get("title", ""),
            company_name=item.get("company", ""),
            company_logo_url=item.get("company_logo_url", ""),
            location=item.get("location", ""),
            salary=item.get("salary", ""),
            job_schedule=item.get("job_schedule", ""),
            job_url=url,
        )

        try:
            await job_listing_service.save(job)
            logger.info(f"✅ Saved job: {job.job_url}")
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения {job.job_url}: {e!r}")

        return item