# -*- coding: utf-8 -*-
import scrapy
import string
from bruter import brute

import bs4
from prnt_sc_collector.items import PrntScCollectorItem

class PrntscSpider(scrapy.Spider):
    name = 'prntsc'
    allowed_domains = ['prnt.sc']
    page_urls = [
        # for testing
        'aa1234'
    ]

    def combiner(self, query):
        self.page_urls.append(query)
        if len(query) > 6:
            exit()

    def start_requests(self):
        symbols = {
            'C': string.ascii_lowercase,
            'N': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        }

        brute("<C><C><N><N><N><N>", self.combiner, symbols)
        print("total of: ", len(self.page_urls))
        for q in self.page_urls:
            yield scrapy.Request(url='https://prnt.sc/' + q, callback=self.parse)

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.body.decode("utf-8", "ignore"), "lxml")
        item = PrntScCollectorItem()
        image = soup.find("img", {"id": "screenshot-image"})
        if image.get('src'):
            file_url = image.get('src')
            item['image_urls'] = [file_url]
            yield item
