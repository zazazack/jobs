# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
from datetime import datetime as dt

import dateparser
from w3lib.html import remove_tags, strip_html5_whitespace
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    city = scrapy.Field()
    company = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    company_score = scrapy.Field()
    id = scrapy.Field()
    job_category = scrapy.Field()
    job_industry = scrapy.Field()
    job_requirements = scrapy.Field()
    job_score = scrapy.Field()
    job_summary = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    post_content = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    job_title = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    normalized_job_title = scrapy.Field()
    job_type = scrapy.Field()  # full-time, part-time, etc.
    location = scrapy.Field()
    organic = scrapy.Field()
    post_age = scrapy.Field()
    post_dt = scrapy.Field()
    post_url = scrapy.Field()
    salary_estimate = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
