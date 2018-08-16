# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime as dt
import hashlib
from pathlib import Path
from urllib.parse import quote, urljoin

import dateparser
import scrapy
import usaddress
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

SETTINGS = get_project_settings()


def post_age_to_datetime(post_age: str) -> str:
    if isinstance(post_age, str):
        dt = dateparser.parse(post_age.replace('+', ''))
        return dt.isoformat(timespec='seconds', sep=' ')


class DropPipeline(object):
    def process_item(self, item, spider):
        if item.get('company') is not None:
            return item
        else:
            raise DropItem(f"Missing company in {item['id']}")



class JobPipeline(object):
    def process_item(self, item, spider):
        if item.get('location') is not None:
            addr = item['location']
            result, result_type = usaddress.tag(addr)
            if result is not None:
                item['city'] = result.get('PlaceName')
                item['state'] = result.get('StateName')
                if result.get('ZipCode') is not None:
                    item['zip_code'] = result.get('ZipCode')

        if item.get('post_age') is not None:
            if "Just posted" in item.get('post_age'):
                item['post_dt'] == dt.datetime.now().isoformat(sep=" ")
            else:
                item['post_dt'] = post_age_to_datetime(item.get('post_age'))

        return item


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    SPLASH_URL = SETTINGS['SPLASH_URL']

    def process_item(self, item, spider):
        query_string = f"/render.png?url={quote(item['url'])}"
        image_url = urljoin(self.SPLASH_URL, query_string)
        request = scrapy.Request(image_url)
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd

    def return_item(self, response, item):
        if response.status != 200:
            # Error happened, return item.
            return item

        # Save screenshot to file, filename will be hash of url.
        url = item["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        p = Path("/usr/src/data/items/images/full/")
        if not p.exists():
            p.mkdir()
        file = p / f'{url_hash}.png'
        file.write_bytes(response.body)

        # Store filename in item.
        item["images"] = file.name
        return item
