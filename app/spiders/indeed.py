# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job, Page, JobLoader

#
# def parse_company(response):
#     for e in response.css('div.result'):
#         for i in e.css('.company *::text').extract():
#             if re.match('\w+', i.strip()):
#                 yield i.strip()
#
#
# def parse_jobtitle(response):
#     for e in response.css('div.result'):
#         for i in e.css('.jobtitle *::text').extract():
#             if re.match('\w+', i.strip()):
#                 yield i.strip()


class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com/jobs?l=houston']
    rules = (
            Rule(LinkExtractor(restrict_css='div.pagination'), follow=True),
            Rule(LinkExtractor(restrict_css='div.result', unique=True), callback='parse_item'),
    )

    def parse_item(self, response):
        """Load items with data scraped from response."""
        loader = JobLoader(item=Job(), response=response)
        loader.add_css('post_url', 'div.result::attr(data-jk)')
        loader.add_css('id', 'div.result::attr(id)')
        result_loader = loader.nested_css('div.result')
        result_loader.add_css('company', '.company *::text')
        result_loader.add_css('post_age', 'span.date::text')
        result_loader.add_css('jobtitle', '.jobtitle *::text')
        result_loader.add_css('location', '.location *::text')
        result_loader.add_css('sponsored', 'span.sponsoredGray::text')
        result_loader.add_css('summary', 'span.summary::text')
        return loader.load_item()

    def parse_page(self, response):
        loader = JobLoader(item=Page(), response=response)
        loader.add_css('page_title', 'title::text')
        return loader.load_item()
