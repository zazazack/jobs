# -*- coding: utf-8 -*-
import json
import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job


class RigzoneSpider(CrawlSpider):
    name = 'rigzone'
    allowed_domains = ['rigzone.com']
    start_urls = ['https://rigzone.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/jobs', deny='/login'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Job()
        try:
            obj = response.css('head > script[type="application/ld+json"]::text').extract_first()
            if obj is not None:
                item['data'] = json.loads(obj.strip())
                if item.get('data') is not None:
                    item['company'] = item.get('data').get('hiringOrganization').get('name')
                    item['title'] = item['data'].get('title')
                    item['country'] = item['data'].get('jobLocation').get('address').get('addressCountry')
                    item['city'] = item['data'].get('jobLocation').get('address').get('addressLocality')
                    item['region'] = item['data'].get('jobLocation').get('address').get('addressRegion')
                    item['post_dt'] = item['data'].get('datePosted')
                    item['description'] = item['data'].get('description')
        except (AttributeError, KeyError, TypeError, json.decoder.JSONDecodeError) as e:
            logging.warning(e)
        return item
