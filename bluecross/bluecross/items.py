import scrapy

class petImage(scrapy.Item):
    petId = scrapy.Field()
    species = scrapy.Field()
    petType = scrapy.Field()
    reserved = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    centre = scrapy.Field()
    info = scrapy.Field()
    height = scrapy.Field()
    dateScraped = scrapy.Field()
    description = scrapy.Field()
