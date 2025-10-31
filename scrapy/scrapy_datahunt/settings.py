BOT_NAME = "scrapy_datahunt"

SPIDER_MODULES = ["scrapy_datahunt.spiders"]
NEWSPIDER_MODULE = "scrapy_datahunt.spiders"

USER_AGENT = "scrapy_datahunt (+https://example.com)"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 1  
CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 4

DOWNLOAD_TIMEOUT = 15
RETRY_ENABLED = True
RETRY_TIMES = 2

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

ITEM_PIPELINES = {
    "scrapy_datahunt.pipelines.ProductPipeline": 300,
}

LOG_LEVEL = "INFO"
FEED_EXPORT_ENCODING = "utf-8"
