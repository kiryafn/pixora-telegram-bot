import logging
from urllib.parse import quote, urlencode

from scrapy import Spider, Request
from bot.scrapers.items.job_listing_item import JobListingItem

class PracujSpider(Spider):
    name = "pracuj"
    allowed_domains = ["pracuj.pl"]

    def __init__(self, keyword: str, location: str, min_salary: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.location = location
        self.min_salary = int(min_salary)
        self.page = 1

    def start_requests(self):
        kw = quote(self.keyword)
        loc = quote(self.location)
        params = {"rd": 0, "sal": self.min_salary, "pn": self.page}
        url = f"https://www.pracuj.pl/praca/{kw};kw/{loc};wp?{urlencode(params)}"

        self.logger.info(f"[PracujSpider] ▶️ стартуем с URL: {url}")

        yield Request(url, callback=self.parse_list, errback=self._err, dont_filter=True)

    def parse_list(self, response):

        self.logger.debug(f"[PracujSpider] получен ответ: {response.status} — {response.url}")

        if response.status != 200:

            self.logger.error(f"[PracujSpider] Ожидал 200, но получил {response.status}")

            return

        nodes = response.css('a[data-test="link-offer"]')

        self.logger.info(f"[PracujSpider] 👉 найдено офферов: {len(nodes)}")

        if not nodes:

            self.logger.warning(f"[PracujSpider] ❌ ничего не найдено на {response.url}")

            return

        for nd in nodes:
            href = nd.attrib.get("href")
            if href:
                yield response.follow(href, callback=self.parse_job, errback=self._err)

        self.page += 1
        kw = quote(self.keyword)
        loc = quote(self.location)
        params = {"rd": 0, "sal": self.min_salary, "pn": self.page}
        next_url = f"https://www.pracuj.pl/praca/{kw};kw/{loc};wp?{urlencode(params)}"

        self.logger.info(f"[PracujSpider] ▶️ следующая страница: {next_url}")

        yield Request(next_url, callback=self.parse_list, errback=self._err, dont_filter=True)

    def parse_job(self, response):
        self.logger.info(f"[PracujSpider] ✏️ JOB {response.status} — {response.url}")
        item = JobListingItem()
        item["url"] = response.url
        item["title"] = response.css(
            "#offer-header > div.cy9wb15 > div > div.oheatec > h1::text"
        ).get(default="").strip()
        item["company"] = response.css(
            "#offer-header > div.cy9wb15 > div > div.oheatec > h2::text"
        ).get(default="").strip()
        item["location"] = response.css(
            "#offer-header > ul.caor1s3 > li:nth-child(1) > div.tchzayo > div.t1g3wgsd > a::text"
        ).get(default="").strip()
        salary = response.css(
            "#offer-header > div.cy9wb15 > div.c1prh5n1 > div > div > div > div.s1n75vtn::text"
        ).get()
        item["salary"] = salary.strip() if salary and salary.strip() else None
        schedule = response.css(
            "#offer-header > ul.caor1s3 > li.fillNth.lowercase.c196gesj > div.tchzayo > div::text"
        ).get()
        item["job_schedule"] = schedule.strip() if schedule and schedule.strip() else "No information"
        yield item

    def _err(self, failure):
        logging.error(f"[PracujSpider] ❗ Ошибка запроса: {failure}")