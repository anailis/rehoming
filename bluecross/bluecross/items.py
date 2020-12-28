import scrapy

class petImage(scrapy.Item):
    petType = scrapy.Field()
    reserved = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    info = scrapy.Field()
    refNum = scrapy.Field()
    dateScraped = scrapy.Field()
    description = scrapy.Field()
