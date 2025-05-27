from typing import Type
from scrapy.spiders import Spider

from bot.scrapers.spiders.pracuj_spider import PracujSpider

COUNTRY_SPIDER_MAP: dict[str, list[Type[Spider]]] = {
    "poland": [PracujSpider],
    "ukraine": [],
}

def get_spiders_for_country(country_name: str) -> list[Type[Spider]]:
    return COUNTRY_SPIDER_MAP.get(country_name.lower(), [])