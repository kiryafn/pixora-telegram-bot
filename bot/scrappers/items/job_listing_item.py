from scrapy import Item, Field


class JobListingItem(Item):
    id: int = Field()
    title: str = Field()
    company: str = Field()
    location: str = Field()
    salary: float = Field(default=None)
    date_posted: str = Field()
    url: str = Field()
