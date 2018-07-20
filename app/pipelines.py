# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import usaddress


class AppPipeline(object):
    def process_item(self, item, spider):
        addr = item['location']
        parsed_addr = usaddress.tag(addr)[0]
        item['zip_code'] = parsed_addr.get('ZipCode')
        item['city'] = parsed_addr.get('PlaceName')
        item['state'] = parsed_addr.get('StateName')
        return item
