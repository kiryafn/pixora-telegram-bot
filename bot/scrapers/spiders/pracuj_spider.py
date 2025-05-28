import logging
from urllib.parse import quote, urlencode

import scrapy
from scrapy import Request, Spider
from bot.scrapers.items.job_listing_item import JobListingItem


class PracujSpider(Spider):
    """
    Scrapy spider for crawling job listings from pracuj.pl.

    The spider starts with a specific job keyword and location, navigates
    through paginated search results, and scrapes details from each job offer.

    Attributes:
        preference_id (int): ID of the job preference used for linking results.
        keyword (str): Combined search keyword (position + company).
        location (str): The city or region to filter job offers.
        min_salary (int): Minimum salary filter for job listings.
        page (int): Current page number in pagination.
    """

    name = "pracuj"
    allowed_domains = ["pracuj.pl"]

    def __init__(
        self,
        preference_id: int,
        position: str,
        company: str,
        location: str,
        min_salary: int,
        *args,
        **kwargs,
    ):
        """
        Initializes the spider with user-defined search preferences.

        Args:
            preference_id (int): The ID used to link found jobs to preferences.
            position (str): Desired job position.
            company (str): Target company name.
            location (str): Location filter for jobs.
            min_salary (int): Minimum salary for filtering results.
        """
        super().__init__(*args, **kwargs)
        self.preference_id = int(preference_id)
        self.keyword = f"{company} {position}"
        self.location = location
        self.min_salary = int(min_salary)
        self.page = 1

    async def start(self):
        """
        Starts the spider by requesting the first page of job listings.
        """
        kw = quote(self.keyword)
        loc = quote(self.location)
        params = {"rd": 0, "sal": self.min_salary, "pn": self.page}
        url = f"https://www.pracuj.pl/praca/{kw};kw/{loc};wp?{urlencode(params)}"

        self.logger.info(f"[PracujSpider] ▶️ starting with URL: {url}")
        yield Request(url, callback=self.parse_list, errback=self._err, dont_filter=True)

    async def parse_list(self, response: scrapy.http.Response):
        """
        Parses a listing page and schedules job offer requests.

        Args:
            response (scrapy.http.Response): The response from the listing page.
        """
        self.logger.debug(f"[PracujSpider] received response: {response.status} — {response.url}")

        if response.status != 200:
            self.logger.error(f"[PracujSpider] expected 200 but got {response.status}")
            return

        hrefs: list[str] = response.css('a[data-test="link-offer"]::attr(href)').getall()
        self.logger.info(f"[PracujSpider] 👉 found offers: {len(hrefs)}")

        if not hrefs:
            self.logger.warning(f"[PracujSpider] ❌ no offers found on {response.url}")
            return

        for href in hrefs:
            yield response.follow(href, callback=self.parse_job, errback=self._err)

        self.page += 1
        kw = quote(self.keyword)
        loc = quote(self.location)
        params = {"rd": 0, "sal": self.min_salary, "pn": self.page}
        next_url = f"https://www.pracuj.pl/praca/{kw};kw/{loc};wp?{urlencode(params)}"

        self.logger.info(f"[PracujSpider] ▶️ next page: {next_url}")
        yield Request(next_url, callback=self.parse_list, errback=self._err, dont_filter=True)

    async def parse_job(self, response: scrapy.http.Response):
        """
        Parses an individual job offer page and extracts job details.

        Args:
            response (scrapy.http.Response): The response from the job detail page.
        """
        self.logger.info(f"[PracujSpider] ✏️ JOB {response.status} — {response.url}")
        item = JobListingItem()

        item["url"] = response.url
        item["title"] = response.css(
            "#offer-header > div.cy9wb15 > div > div.oheatec > h1::text"
        ).get(default="NA").strip()
        item["company"] = response.css(
            "#offer-header > div.cy9wb15 > div > div.oheatec > h2::text"
        ).get(default="NA").strip()
        item["company_logo_url"] = response.css(
            "#offer-header > div.cy9wb15 > div.cmqurxq > div.l1d9j6zz > picture > img::attr(src)"
        ).get(
            default="https://img.freepik.com/premium-vector/no-photo-available-vector-icon-default-image-symbol-picture-coming-soon-web-site-mobile-app_87543-18055.jpg"
        ).strip()
        item["location"] = response.css(
            "#offer-header > ul.caor1s3 > li:nth-child(1) > div.tchzayo > div.t1g3wgsd > a::text"
        ).get(default=self.location).strip()
        item["salary"] = response.css(
            "#offer-header > div.cy9wb15 > div.c1prh5n1 > div > div > div > div.s1n75vtn::text"
        ).get(default="NA").strip()
        item["job_schedule"] = response.css(
            "#offer-header > ul.caor1s3 > li.fillNth.lowercase.c196gesj > div.tchzayo > div::text"
        ).get(default="NA").strip()

        yield item

    async def _err(self, failure):
        """
        Error handler for failed requests.

        Args:
            failure: The request failure object.
        """
        logging.error(f"[PracujSpider] ❗ Request failed: {failure}")