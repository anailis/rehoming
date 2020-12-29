import scrapy
from ..items import petImage

from datetime import date

class BluecrossSpider(scrapy.Spider):
    name = "bluecross"

    def start_requests(self):
        urls = [
            'https://www.bluecross.org.uk/rehome/dog',
            'https://www.bluecross.org.uk/rehome/horse'
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

        petType = response.xpath('//li[@class="pet-details_species"]/text()').get().strip().split()
        indiv['species'] = petType[0]
        indiv['petType'] = " ".join(petType[2:])

        indiv['sex'] = response.xpath('//li[@class="pet-details_sex"]/text()').get().strip()
        indiv['age'] = response.xpath('//li[@class="pet-details_age"]/text()').get().strip()
        indiv['centre'] = response.xpath('//li[@class="pet-details_location"]/a/text()').get().strip()

        petId = response.xpath('//li[@class="pet-details_reference"]/text()').get().strip()
        indiv['petId'] = "".join([s for s in petId.split() if s.isdigit()])

        indiv['dateScraped'] = date.today()

        height = response.xpath('//li[@class="pet-details_height"]/text()').get()
        if height:
            indiv['height'] = height.strip()
        else:
            indiv['height'] = None

        indiv['reserved'] = bool(response.xpath('//div[@class="banner banner--reserved"]/span/text()').get())

        info = response.xpath('//li[@class="pet-details_info"]/text()[preceding-sibling::br]').get()
        if info:
            indiv['info'] = info.strip()
        else:
            indiv['info'] = None

        indiv['description'] = " ".join(response.xpath('//div[@class="column-main"]/p/text()').getall())

        yield indiv