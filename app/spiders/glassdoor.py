# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.items import Job, JobLoader


class GlassdoorSpider(CrawlSpider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    start_urls = ['https://www.glassdoor.com']
    rules = (
        Rule(LinkExtractor(allow=('/Job', 'job-listing')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        loader = JobLoader(item=Job(), response=response)
        result_loader = loader.nested_css('li.jl')
        result_loader.add_css('normalized_job_title', '::attr(data-normalize-job-title)')
        result_loader.add_css('company', '.empLoc > div::text')
        result_loader.add_css('id', '::attr(data-id)')
        result_loader.add_css('job_title', 'a::text')
        result_loader.add_css('location', '.loc::text')
        result_loader.add_css('organic', '::attr(data-is-organic-job)')
        result_loader.add_css('post_age', 'span.minor::text')
        result_loader.add_value('post_url', response.urljoin(response.css('a::attr(href)').extract_first())
        loader.add_css('post_content', 'div.jobDescriptionContent')
        return loader.load_item()
