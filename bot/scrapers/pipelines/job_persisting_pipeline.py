import asyncio

from bot.models.job_listing import JobListing
from bot.scrapers.items.job_listing_item import JobListingItem
from bot.services import job_listing_service

#todo if a job listing under this url exists in the db, we should update it

class JobListingServicePipeline:

    def process_item(self, item: JobListingItem, spider) -> JobListingItem:
        job = JobListing(
            id=int(item['id']),
            job_title=item['title'],
            company_name=item['company'],
            location=item['location'],
            salary=float(item['salary']) if item.get('salary') is not None else 0.0,
            job_url=item['url'],
            date_posted=item.get('date_posted')
        )

        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(job_listing_service.save_job_listing(job))
        else:
            loop.run_until_complete(job_listing_service.save_job_listing(job))
        return item