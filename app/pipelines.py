# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import usaddress
import dateparser


def post_age_to_datetime(post_age: str) -> str:
    if isinstance(post_age, str):
        dt = dateparser.parse(post_age.replace('+', ''))
        return dt.isoformat(timespec='seconds', sep=' ')


class AppPipeline(object):
    def process_item(self, item, spider):
        if item.get('location') is not None:
            addr = item['location']
            result, result_type = usaddress.tag(addr)
            if result is not None:
                item['zip_code'] = result.get('ZipCode')
                item['city'] = result.get('PlaceName')
                item['state'] = result.get('StateName')

        if item.get('post_age') is not None:
            item['post_dt'] = post_age_to_datetime(item.get('post_age'))

        return item
