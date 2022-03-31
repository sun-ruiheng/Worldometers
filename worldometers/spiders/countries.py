
import scrapy

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a/text()").getall()

        # yield {
        #     'title': title,
        #     'countries': countries
        # }

        print({
            'title': title,
            'countries': countries
            })

        # I am using print instead of yield when calling from the scheduler file, countries_scheduled.

