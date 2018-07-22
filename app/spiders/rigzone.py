# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job, JobLoader

class RigzoneSpider(CrawlSpider):
    name = 'rigzone'
    allowed_domains = ['rigzone.com']
    start_urls = ['http://rigzone.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/jobs'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        loader = JobLoader(item=Job(), selector=response.css('article'), response=response)
        loader.add_css('job_title', 'h3 > a::text')
        loader.add_css('post_url', 'h3 > a::attr(href)')
        loader.add_xpath('location', '//address')
        loader.add_css('company', 'address::text')
        loader.add_css
        return loader.load_item()
