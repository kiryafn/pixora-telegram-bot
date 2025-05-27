from scrapy import Item, Field

class JobListingItem(Item):
    title: str = Field()
    company: str = Field()
    company_logo_url: str = Field()
    location: str = Field()
    salary: str = Field()
    job_schedule: str = Field()
    url: str = Field()
