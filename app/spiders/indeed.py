# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import Join
from app.items import Job, JobLoader
from w3lib.html import remove_tags


class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com']
    rules = (
            Rule(LinkExtractor(allow=('/jobs')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """Load items with data scraped from response."""
        loader = JobLoader(item=Job(), response=response)
        loader.add_css('id', 'div.result::attr(id)')
        result_loader = loader.nested_css('div.result')
        result_loader.add_css('company', '.company::text')
        result_loader.add_css('post_age', 'span.date::text')
        result_loader.add_css('title', '.jobtitle::text')
        result_loader.add_css('location', '.location *::text')
        result_loader.add_xpath('description', "normalize-space(//span[@class='summary']/text())", output_processor=Join())
        return loader.load_item()
