import scrapy
from ..items import petImage

from datetime import date

class PetsSpider(scrapy.Spider):
    name = "pets"

    def start_requests(self):
        urls = [
            'https://www.bluecross.org.uk/rehome/dog'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.getURL)

    def getURL(self, response):
        petLinks = response.xpath('//a[@class="item__link"]/@href').getall()
        for link in petLinks:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        indiv = petImage()
        indiv['petType'] = response.xpath('//li[@class="pet-details_species"]/text()').get().strip()
        indiv['sex'] = response.xpath('//li[@class="pet-details_sex"]/text()').get().strip()
        indiv['age'] = response.xpath('//li[@class="pet-details_age"]/text()').get().strip()
        indiv['location'] = response.xpath('//li[@class="pet-details_location"]/a/text()').get().strip()
        indiv['refNum'] = response.xpath('//li[@class="pet-details_reference"]/text()').get().strip()
        indiv['dateScraped'] = date.today()

        indiv['reserved'] = bool(response.xpath('//div[@class="banner banner--reserved"]/span/text()').get())

        info = response.xpath('//li[@class="pet-details_info"]').get()
        if info:
            indiv['info'] = info.strip()
        else:
            indiv['info'] = None

        indiv['description'] = " ".join(response.xpath('//div[@class="column-main"]/p/text()').getall())
        yield indiv