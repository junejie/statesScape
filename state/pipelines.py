from scrapy.http import Request
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StatePipeline(object):
    def process_item(self, item, spider):
        print 'xxx >> ',item
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print 'image_url:', image_url
            yield Request(image_url)
