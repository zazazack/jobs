# -*- coding: utf-8 -*-
from urllib.parse import quote

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import Join
from app.items import Job, JobLoader
from scrapy.utils.project import get_project_settings

SETTINGS = get_project_settings()
SPLASH_URL = SETTINGS['SPLASH_URL']

class IndeedSpider(CrawlSpider):
    name = 'indeed'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com/jobs?l=Houston,TX']
    rules = (
            Rule(LinkExtractor(allow=(r'/jobs')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """Load items with data scraped from response."""
        loader = JobLoader(item=Job(), response=response)
        loader.add_css('id', 'div.result::attr(id)')
        loader.add_value('image_url', f"http://localhost:8050/render.png?url={quote(response.url)}")
        result_loader = loader.nested_css('div.result')
        result_loader.add_css('company', '.company::text')
        result_loader.add_css('post_age', 'span.date::text')
        result_loader.add_css('title', '.jobtitle::text')
        result_loader.add_css('location', '.location *::text')
        result_loader.add_xpath('description', "normalize-space(//span[@class='summary']/text())", output_processor=Join())
        return loader.load_item()
