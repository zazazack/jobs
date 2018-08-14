# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.parse import quote, urljoin
from pathlib import Path
import dateparser
import scrapy
import hashlib
import usaddress

from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest


SETTINGS = get_project_settings()


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


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    SPLASH_URL = SETTINGS['SPLASH_URL']

    def process_item(self, item, spider):
        screenshot_url = urljoin(self.SPLASH_URL, f"/render.png?url={quote(item['url'])}")
        request = scrapy.Request(screenshot_url)
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
        p = Path("/usr/src/items/images/full/")
        if not p.exists():
            p.mkdir()
        file = p / f'{url_hash}.png'
        file.write_bytes(response.body)

        # Store filename in item.
        item["images"] = file.name
        return item
