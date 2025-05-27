from scrapy import Item, Field


class JobListingItem(Item):
    title: str = Field()
    company: str = Field()
    location: str = Field()
    salary: float = Field(default=None)
    #date_posted: str = Field()
    job_schedule: str = Field()
    url: str = Field()
