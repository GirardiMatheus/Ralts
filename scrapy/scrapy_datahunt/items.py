import scrapy

class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    db_id = scrapy.Field()
