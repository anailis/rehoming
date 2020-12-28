import scrapy

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
        species = response.xpath('//li[@class="pet-details_species"]').get()
        filename = 'bluecross_test.txt'
        with open(filename, 'w') as f:
            f.write(species)
        self.log(f'Saved file {filename}')