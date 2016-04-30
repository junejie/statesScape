# -*- coding: utf-8 -*-
import scrapy
import time
from state.items import StateItem
from state.pipelines import StatePipeline

class StatespiderSpider(scrapy.Spider):
    name = "statespider"
    allowed_domains = ["www.state.gov"]
    start_urls = (
        'http://www.state.gov/misc/list/',
    )

    def parse(self, response):
        for url in response.xpath('//html/body/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td/div/div/div/div/blockquote/p/a/text()').extract():
            yield { "c": url}

        for url in response.xpath('//html/body/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td/div/div/div/div/blockquote/p/a/@href'):
            url = response.urljoin(url.extract())
            yield scrapy.Request(url, callback=self.proc_url)

    def proc_url(self, response):
        print 'data::::', response
        d = StatePipeline()
        
        for i in response.xpath(".//*[@id='tier3-landing-content']/p[2]/img/@src"):
            img= i.extract()
            item = StateItem()
            item['image_urls']  ='http://www.state.gov'+img
            item['images']  = str(time.time())
            d.process_item(self, item )