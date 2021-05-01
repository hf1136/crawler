import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    #allowed_domains = ['example.com']
    start_urls = ['https://www.javbus.com/']

    def parse(self, response):
        #print(response.text)
        pass
