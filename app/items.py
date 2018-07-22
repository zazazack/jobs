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


def build_post_url(jobkey):
    return f'https://www.indeed.com/viewjob?jk={jobkey}'


def post_age_to_datetime(post_age: str) -> str:
    if isinstance(post_age, str):
        dt = dateparser.parse(post_age.replace('+', ''))
        return dt.isoformat(timespec='seconds', sep=' ')


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    id = scrapy.Field()
    post_age = scrapy.Field()
    post_dt = scrapy.Field(input_processor=MapCompose(post_age_to_datetime))
    post_url = scrapy.Field(input_processor=MapCompose(build_post_url))
    company = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    company_score = scrapy.Field()
    job_category = scrapy.Field()
    job_industry = scrapy.Field()
    job_requirements = scrapy.Field()
    job_score = scrapy.Field()
    job_summary = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    job_title = scrapy.Field(input_processor=MapCompose(remove_tags, strip_html5_whitespace))
    job_type = scrapy.Field()  # full-time, part-time, etc.
    salary_estimate = scrapy.Field()
    location = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
