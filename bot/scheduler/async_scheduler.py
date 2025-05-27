import logging
import asyncio
from datetime import datetime, timedelta

from twisted.internet import asyncioreactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging

from bot.services import job_preference_service
from bot.scrapers import settings as project_settings
from bot.scrapers.registry import get_spiders_for_country

asyncioreactor.install()

configure_logging()
_settings = Settings()
_settings.setmodule(project_settings)

_runner = CrawlerRunner(_settings)

logger = logging.getLogger(__name__)

async def crawl_preference(pref) -> None:
    country = pref.city.country.name
    spiders = get_spiders_for_country(country)
    logger.info(f"[crawl_preference] pref_id={pref.id!r} country={country!r} → spiders={spiders!r}")

    if not spiders:
        logger.warning(f"[crawl_preference] No spiders for country {country!r}")
        return

    deferreds = [
        _runner.crawl(
            spider_cls,
            keyword=pref.title,
            location=pref.city.name,
            min_salary=pref.min_salary,
        )
        for spider_cls in spiders
    ]
    await asyncio.gather(*[deferred_to_future(d) for d in deferreds])

async def scrape_all_preferences() -> None:
    try:
        prefs = await job_preference_service.get_all()
        tasks = [asyncio.create_task(crawl_preference(pref)) for pref in prefs]
        if tasks:
            await asyncio.gather(*tasks)
    except Exception:
        logger.exception("Error in scrape_all_preferences")

async def scheduler_loop() -> None:
    while True:
        now = datetime.now()
        next_run = now.replace(minute=24, second=0, microsecond=0)
        if next_run <= now:
            next_run += timedelta(hours=1)
        wait_seconds = (next_run - now).total_seconds()

        logger.info(f"Next crawl scheduled at {next_run.isoformat()} UTC (in {wait_seconds:.0f}s)")
        await asyncio.sleep(wait_seconds)

        await scrape_all_preferences()

def start_asyncio_scheduler() -> None:
    asyncio.create_task(scheduler_loop())
    logger.info("🕒 AsyncIO scheduler started")