from scrapy.http import Request
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StatePipeline(object):
    def process_item(self, item, spider):
        print 'xxx >> ',item
        return self.get_media_requests( item,spider)

    def get_media_requests(self, item, info):
        print 'get_media_requests'
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        print 'item_completed'
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item