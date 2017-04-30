'''Conor Campbell - CSCE 590 Final Project'''
import scrapy
import csv

class Twitter(scrapy.Spider):
    name = "twitter"

    start_urls = [
        'http://friendorfollow.com/twitter/most-followers/',
    ]

    def parse(self, response):
        # Use xpath to get names and handles of twitter users. 
        allPeopleNames = response.xpath('//ul[@class="view-list"]/li/div[@class="text-holder"]/h3/text()').extract()
        allPeopleHandles = response.xpath('//ul[@class="view-list"]/li/div[@class="text-holder"]/p[@class="mail"]/a/text()').extract()

        for i, name in enumerate(allPeopleNames):
            index = name.find('.')
            name = name[index + 2:]
            allPeopleNames[i] = name

        fullList = list(zip(allPeopleNames, allPeopleHandles))
        print(fullList)

        myfile = open('../twitterData.csv', 'w')
        wr = csv.writer(myfile)
        wr.writerow(['Name', 'Handle'])
        for element in fullList:
            wr.writerow([element[0], element[1]])
