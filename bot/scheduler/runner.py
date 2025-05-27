from twisted.internet import asyncioreactor
asyncioreactor.install()

import asyncio
import logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

from bot.scrapers import settings as project_settings
from bot.scrapers.registry import get_spiders_for_country

configure_logging()
_settings = Settings()
_settings.setmodule(project_settings)
log = logging.getLogger("apscheduler")
log.debug(
    f"Loaded Scrapy settings: USER_AGENT={_settings.get('USER_AGENT')!r}, "
    f"COOKIES_ENABLED={_settings.get('COOKIES_ENABLED')!r}, "
    f"ROBOTSTXT_OBEY={_settings.get('ROBOTSTXT_OBEY')!r}"
)

_runner = CrawlerRunner(_settings)

async def crawl_preference(pref) -> None:
    logger = logging.getLogger("apscheduler")
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