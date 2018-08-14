# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from datetime import datetime as dt
import json
from pathlib import Path
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags
from scrapy_jsonschema.item import JsonSchemaItem


def get_digits(text):
    return "".join(s for s in text if s.isdigit())


def normalize_text(s):
    if isinstance(s, str):
        return s.strip().casefold()


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    city = scrapy.Field()
    company = scrapy.Field()
    company_score = scrapy.Field()
    id = scrapy.Field(input_processor=Identity())
    description = scrapy.Field()
    job_category = scrapy.Field()
    job_description = scrapy.Field()
    job_experience = scrapy.Field()
    job_industry = scrapy.Field()
    job_requirements = scrapy.Field()
    job_score = scrapy.Field()
    job_summary = scrapy.Field()
    job_title = scrapy.Field()
    job_type = scrapy.Field()  # full-time, part-time, etc.
    location = scrapy.Field()
    normalized_job_title = scrapy.Field()
    organic = scrapy.Field()
    post_age = scrapy.Field()
    post_dt = scrapy.Field()
    post_url = scrapy.Field()
    response_url = scrapy.Field()
    salary_estimate = scrapy.Field()
    spider = scrapy.Field()
    state = scrapy.Field()
    timestamp = scrapy.Field(input_processor=Identity())
    url = scrapy.Field()
    screenshot = scrapy.Field()
    image_url = scrapy.Field()
    images = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    data = scrapy.Field()
    zip_code = scrapy.Field()
