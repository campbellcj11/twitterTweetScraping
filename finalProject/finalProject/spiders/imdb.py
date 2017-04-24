import scrapy
import csv

class imdbSpider(scrapy.Spider):
    name = "imdb"

    start_urls = [
        'http://www.imdb.com/list/ls054840033/',
    ]

    def parse(self, response):
        allActors = response.xpath('//div[@class="info"]/b/a/text()').extract()
        print(allActors)
        for element in allActors:
            print(element)
