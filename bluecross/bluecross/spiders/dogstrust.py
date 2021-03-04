import scrapy
from ..items import petImage

import re
from datetime import date

class DogstrustSpider(scrapy.Spider):
    name = "dogstrust"

    def start_requests(self):
        urls = [
            'https://www.dogstrust.org.uk/rehoming/dogs/filters/~~~~~n~~'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.getURL)

    def getURL(self, response):
        nextPage = response.xpath('//div[@class="controls__buttons"]//a[@id="BodyContent_DogList1_lnkNext"]//@href').get()
        if nextPage:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.getURL)

        petLinks = response.xpath('//div[@class="grid grid--fix grid--large grid--blank"]//a/@href').getall()
        for link in petLinks:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        indiv = petImage()

        indiv['species'] = "Dog"

        centre_and_breed = response.xpath('//div[@class="dog-meta__value"]/a/text()').getall()
        indiv['centre'] = centre_and_breed[0].strip()
        indiv['petType'] = centre_and_breed[1].strip()

        age_and_sex = response.xpath('//div[@class="dog-meta__value"]/text()').getall()
        age_and_sex = [value.strip() for value in age_and_sex if value.strip()]
        indiv['sex'] = age_and_sex[1]
        indiv['age'] = age_and_sex[0]

        petId = re.search("n~~/(.*)/", response.request.url).group(1)
        indiv['petId'] = "DT" + petId

        indiv['dateScraped'] = date.today()

        description = response.xpath('//div[@class="dog-profile"]//p//text()').getall()
        if description:
            indiv['description'] = " ".join([value.strip() for value in description if value.strip()])
            print(indiv['description'])
        else:
            indiv['description'] = "NA"

        indiv['reserved'] = 1
        indiv['info'] = "NA"
        indiv['height'] = None

        yield indiv
