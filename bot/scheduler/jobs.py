import logging
import asyncio
from asyncio import Task

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.services import job_preference_service
from bot.scheduler.runner import crawl_preference

sched = AsyncIOScheduler(timezone="UTC")
sched.configure(logger=logging.getLogger("apscheduler"))


async def scrape_all_preferences() -> None:
    prefs = await job_preference_service.get_all()
    tasks: list[Task[None]] = []

    for pref in prefs:
        tasks.append(asyncio.create_task(crawl_preference(pref)))

    if tasks:
        await asyncio.gather(*tasks)


def start_scheduler() -> None:
    sched.add_job(scrape_all_preferences, "cron", minute="05")
    sched.start()