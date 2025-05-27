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
            existing.job_title = item.get("title", existing.job_title)
            existing.company_name = item.get("company", existing.company_name)
            existing.location = item.get("location", existing.location)
            if item.get("salary"):
                try:
                    existing.salary = float(item["salary"].replace("\u00a0", "").replace(",", "."))
                except Exception:
                    logger.warning(f"Не удалось преобразовать зарплату '{item['salary']}' для {url}, оставляем прежнее значение {existing.salary}")
            existing.job_schedule = item.get("job_schedule", existing.job_schedule)
            job = existing
        else:
            salary_val = 0.0
            if item.get("salary"):
                try:
                    salary_val = float(item["salary"].replace("\u00a0", "").replace(",", "."))
                except Exception:
                    logger.warning(f"Не удалось преобразовать зарплату '{item['salary']}' для {url}, устанавливаем 0.0")
            job = JobListing(
                job_title    = item.get("title", ""),
                company_name = item.get("company", ""),
                location     = item.get("location", ""),
                salary       = salary_val,
                job_schedule = item.get("job_schedule", ""),
                job_url      = url,
            )

        try:
            await job_listing_service.save(job)
            logger.info(f"✅ Saved job: {job.job_url}")
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения {job.job_url}: {e!r}")

        return item