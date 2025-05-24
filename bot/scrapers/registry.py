from typing import Type, List
from scrapy.spiders import Spider

from bot.scrapers.spiders.pracuj_spider import PracujSpider

_SPIDER_MAP: dict[str, List[Type[Spider]]] = {
    "Poland": [PracujSpider],
    "Ukraine": [],
}


def get_spiders_for_country(country_name: str) -> List[Type[Spider]]:
    return _SPIDER_MAP.get(country_name, [])