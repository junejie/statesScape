# -*- coding: utf-8 -*-
import scrapy
import time
import urlparse
from state.items import StateItem
from state.pipelines import StatePipeline

class StatespiderSpider(scrapy.Spider):
    name = "statespider"
    allowed_domains = ["www.state.gov"]
    start_urls = [
        'http://www.state.gov/misc/list/'
    ]
    

    def parse(self, response):
        allStates = response.xpath('//html/body/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td/div/div/div/div/blockquote/p/a/text()').extract()
        
        allFlag = response.xpath('//html/body/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td/div/div/div/div/blockquote/p/a/@href')
        
        #validate all flag is equal to state
        print len(allStates), len(allFlag)

        flagNumber = 0       
        for url in allFlag:
            url = response.urljoin(url.extract())
            flag = scrapy.Request(url, callback=self.proc_url)

            #extra data save to meta
            flag.meta['item'] = {'state':allStates[flagNumber]}

            #iterate val for meta
            flagNumber = flagNumber+1
            
            yield flag

    def proc_url(self, response):
        print 'response::::', response.meta['item']
        
        for images in response.xpath(".//*[@id='tier3-landing-content']/p[2]/img/@src"):
            img = [ 'http://www.state.gov/' + images.extract()[1:]]
            item = StateItem()            
            item['image_urls']  = img

            # this data is from meta
            item['state']  = response.meta['item']
            item['images']  = str(time.time())
            print 'data-1:::;',images
            yield item