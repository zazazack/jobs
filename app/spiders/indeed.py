# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job, JobLoader


class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com/jobs?l=houston']
    rules = (
        Rule(LinkExtractor(restrict_css='div.pagination > a'),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        """Load items with data scraped from response."""
        loader = JobLoader(item=Job(), response=response)
        result_loader = loader.nested_css('div.row.result')
        result_loader.add_css('company', 'span.company::text')
        result_loader.add_css('date', 'span.date::text')
        result_loader.add_css('href', 'a.jobtitle::attr(href)')
        result_loader.add_css('jobtitle', 'a.jobtitle::attr(title)')
        result_loader.add_css('sponsored', 'span.sponsoredGray::text')
        result_loader.add_css('summary', 'span.summary::text')
        return loader.load_item()
