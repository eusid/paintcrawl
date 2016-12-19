# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from paint.items import PaintItem
import time

class PaintersSpider(scrapy.Spider):
    name = "painters"
    allowed_domains = ["painters.org"]
    start_urls = ['http://www.painters.org/painters-FL-Florida/']

    def parse_business(self, response):
        sel = Selector(response)
        content = sel.css('div.mcbox-bizdetails')
        item = PaintItem()
        if content.css('p::text').extract_first() is not None:
            item['name'] = content.css('p::text').extract_first()
            item['address'] = content.css('p:nth-child(n+2)::text').extract_first()
            item['postal_code'] = content.css('p:nth-child(n+3)::text').extract_first()
            item['phone'] = content.css('p:nth-child(n+4)::text').extract_first()
            yield item

    def parse_city(self, response):
        sel = Selector(response)
        content = sel.css('div.mcbox-bizlist')
        for link in content.css('a::attr(href)').extract():
            if not '.php' in link:
                url = response.urljoin(link)
                time.sleep(1)
                yield Request(url, callback=self.parse_business)

    def parse(self, response):
        sel = Selector(response)
        content = sel.css('div.middlecolumn')
        for link in content.css('a::attr(href)').extract():
            if 'city' in link:
                url = response.urljoin(link)
                city = link[5:]
                city = city[:-1]
                if city != 'Fort Myers-FL' or 'Fort Myers Beach-FL' or 'Tampa-FL':
                    time.sleep(1)
                    yield Request(url, callback=self.parse_city)
