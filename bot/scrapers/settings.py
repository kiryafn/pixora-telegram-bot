BOT_NAME = "bot_scrapers"

SPIDER_MODULES = ["bot.scrapers.spiders"]
NEWSPIDER_MODULE = "bot.scrapers.spiders"

ITEM_PIPELINES = {
    "bot.scrapers.pipelines.JobListingServicePipeline": 300,
}

DOWNLOADER_MIDDLEWARES = {
}

SPIDER_MIDDLEWARES = {
}

EXTENSIONS = {
}

LOG_ENABLED = True
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(levelname)s: %(message)s"


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1.0
CONCURRENT_REQUESTS_PER_DOMAIN = 8