# -*- coding: utf-8 -*-
import json
import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Identity, TakeFirst
from w3lib.html import remove_tags, strip_html5_whitespace

from app.items import Job, JobLoader


class RigzoneSpider(CrawlSpider):
    name = 'rigzone'
    allowed_domains = ['rigzone.com']
    start_urls = ['https://rigzone.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/jobs'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Job()
        try:
            obj = response.css('head > script[type="application/ld+json"]::text').extract_first()
            if obj is not None:
                item['data'] = json.loads(obj.strip())
        except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
            logging.warning(e)
        return item
