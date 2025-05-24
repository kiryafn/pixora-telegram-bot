from urllib.parse import urlencode
from typing import Generator, Optional, Dict, Any

from scrapy import Spider, Request, Response

from bot.scrapers.items.job_listing_item import JobListingItem

#todo если нет подходящих вакансий не возвращать ничего
#todo сделать обработку по названию компанииё

class PracujSpider(Spider):
    name: str = "pracuj"
    allowed_domains: list[str] = ["pracuj.pl"]

    def __init__(
            self,
            keyword: str,
            location: str,
            min_salary: int,
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.keyword: str = keyword
        self.location: str = location
        self.min_salary: int = min_salary
        self.page: int = 1

    def start_requests(self) -> Generator[Request, None, None]:
        base: str = f"https://www.pracuj.pl/praca/{self.keyword};kw/{self.location};wp"
        params: Dict[str, Any] = {"rd": 0, "sal": self.min_salary, "pn": self.page}
        query: str = urlencode(params)
        url: str = f"{base}?{query}"
        yield Request(url, callback=self.parse_list)

    def parse_list(self, response: Response) -> Generator[Request, None, None]:
        offers = response.css("article.offer")
        for offer in offers:
            href: Optional[str] = offer.css(
                "a.offer-details__title-link::attr(href)"
            ).get()
            if href:
                yield response.follow(href, callback=self.parse_job)

        if offers:
            self.page += 1
            base = f"https://www.pracuj.pl/praca/{self.keyword};kw/{self.location};wp"
            params = {"rd": 0, "sal": self.min_salary, "pn": self.page}
            next_query = urlencode(params)
            next_url = f"{base}?{next_query}"
            yield Request(next_url, callback=self.parse_list)

    def parse_job(self, response: Response) -> Generator[JobListingItem, None, None]:
        item = JobListingItem()
        item["url"] = response.url
        item["id"] = response.url.rstrip("/").split("/")[-1]
        item["title"] = response.css("h1::text").get(default="").strip()
        item["company"] = response.css(
            "a.offer-company__name::text"
        ).get(default="").strip()
        item["location"] = response.css(
            "li.offer-features__item-location::text"
        ).get(default="").strip()
        salary_text: Optional[str] = response.css(
            "span.offer-salary span::text"
        ).get()
        item["salary"] = salary_text.strip() if salary_text else None
        item["date_posted"] = response.css("time::attr(datetime)").get()
        yield item
