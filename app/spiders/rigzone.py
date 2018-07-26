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
        l = JobLoader(item=Job(), selector=response.css('div#content'))
        article_loader = l.nested_css('article.update-block.current')
        heading_loader = article_loader.nested_css('div.heading')
        heading_loader.add_css('job_title', 'a::text')
        heading_loader.add_css('id', '.rating *::attr(id)')
        heading_loader.add_css('company', 'address::text')
        heading_loader.add_xpath('location', 'normalize-space(.//address)')
        description_loader = l.nested_css('article.description')
        description_loader.add_css('job_experience', 'span.experience::text')
        description_loader.add_css('post_age', 'time::attr(datetime)')
        return l.load_item()
