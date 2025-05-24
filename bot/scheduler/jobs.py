import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.services.job_preference_service import job_preference_service
from bot.services.job_listing_service import job_listing_service
from bot.scheduler.runner import crawl_preference

sched = AsyncIOScheduler(timezone="UTC")
sched.configure(logger=logging.getLogger("apscheduler"))


async def scrape_all_preferences() -> None:
    prefs = await job_preference_service.get_all()
    for pref in prefs:
        marker = f"pref:{pref.id}"
        await job_listing_service.mark_all_not_seen(pref.id)
        await crawl_preference(pref, seen_marker=marker)
        await job_listing_service.expire_not_seen(pref.id, marker)


def start_scheduler() -> None:
    sched.add_job(scrape_all_preferences, "cron", minute="40")
    sched.start()