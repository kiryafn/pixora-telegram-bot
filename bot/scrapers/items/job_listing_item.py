from scrapy import Item, Field

class JobListingItem(Item):
    """
    Scrapy item representing a job listing scraped from a website.

    Attributes:
        title (str): The job title or position name.
        company (str): The name of the company offering the job.
        company_logo_url (str): URL of the company's logo image.
        location (str): Location of the job (e.g., city, remote).
        salary (str): Salary information or compensation range.
        job_schedule (str): Schedule type (e.g., full-time, part-time).
        url (str): URL of the original job listing page.
    """

    title: str = Field()
    company: str = Field()
    company_logo_url: str = Field()
    location: str = Field()
    salary: str = Field()
    job_schedule: str = Field()
    url: str = Field()