import asyncio
from typing import Type, List
from twisted.internet import asyncioreactor

asyncioreactor.install(asyncio.get_event_loop())

from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.defer import maybe_deferred_to_future

from bot.scrapers import settings as project_settings
from bot.scrapers.registry import get_spiders_for_country

configure_logging()

_settings = Settings()
_settings.setmodule(project_settings)

_runner = CrawlerRunner(_settings)


async def crawl_preference(pref, seen_marker: str) -> None:
    spiders: List[Type[Spider]] = get_spiders_for_country(pref.city.country.name)
    if not spiders:
        return

    deferreds = []
    for spider_cls in spiders:
        deferreds.append(
            _runner.crawl(
                spider_cls,
                keyword=pref.title,
                location=pref.city.name,
                min_salary=pref.min_salary,
                seen_marker=seen_marker,
            )
        )

    futures = [maybe_deferred_to_future(d) for d in deferreds]
    await asyncio.gather(*futures)
