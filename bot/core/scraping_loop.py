import logging
import asyncio
from datetime import datetime, timedelta

from twisted.internet import asyncioreactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging

from bot.services.job_preference_service import job_preference_service
from bot.scrapers import settings as project_settings
from bot.scrapers.spiders import PracujSpider

# patch Twisted → asyncio
asyncioreactor.install()
configure_logging()

_settings = Settings()
_settings.setmodule(project_settings)
_runner = CrawlerRunner(_settings)
_log = logging.getLogger(__name__)


async def _crawl_all_preferences() -> None:
    prefs = await job_preference_service.get_all()
    if not prefs:
        _log.info("⏳ No job preferences found, skipping crawl.")
        return

    futures = []
    for p in prefs:
        country = p.city.country.name
        _log.info(f"▶️  scheduling crawl for pref_id={p.id!r} country={country!r}")

        d = _runner.crawl(
            PracujSpider,
            preference_id=p.id,
            position=p.title,
            company=p.company or "",
            location=p.city.name,
            min_salary=p.min_salary,
        )
        futures.append(deferred_to_future(d))

    await asyncio.gather(*futures)


async def scheduler_loop() -> None:
    while True:
        now = datetime.utcnow()
        # schedule at :30 every hour
        next_run = now.replace(minute=30, second=0, microsecond=0)
        if next_run <= now:
            next_run += timedelta(hours=1)
        wait = (next_run - now).total_seconds()

        _log.info(f"🕒 Next crawl at {next_run.isoformat()} UTC (in {wait:.0f}s)")
        await asyncio.sleep(wait)

        try:
            await _crawl_all_preferences()
        except Exception:
            _log.exception("❌ Unhandled error during scheduled crawl")


def periodic_crawl() -> None:
    """Start the background scheduler on the existing event loop."""
    asyncio.create_task(scheduler_loop())
    _log.info("✅ AsyncIO-based scraper scheduler started")