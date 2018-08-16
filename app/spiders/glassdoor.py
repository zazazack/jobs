# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job, JobLoader


class GlassdoorSpider(CrawlSpider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com']
    rules = (
        Rule(LinkExtractor(allow=('/Job')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Job()
        for e in response.css('li.jl'):
            item['company'] = e.css('div.empLoc ::text').re('\s+(.*)\s+–')[0]
            item['easy_apply'] = e.css('div.easyApply::text').extract_first()
            item['id'] = e.css('::attr(data-id)').extract_first()
            item['title'] = e.css('a.jobLink::text').extract_first()
            item['location'] = e.css('span.loc::text').extract_first()
            item['post_age'] = e.css('span.minor::text').extract_first()
        return item
