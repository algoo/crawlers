# -*- coding: utf-8 -*-

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import urlparse
from scrapy.utils.response import get_base_url

from scrapy import Spider, Item, Field, Request

class Tag(object):
    def __init__(self, tag, iteration_nb=1):
        self.tag = tag
        self.weight = iteration_nb

class JobSpider(Spider):

    start_urls = []  # To be overwritten
    name = 'no-name'  # To be overwritten

    COMMON_TAGS = [
        u'cdi', u'cdd', u'télétravail', u'stage', u'freelance', u'mysql'
        u'postgresql', u'django'
    ]
    def _build_url(self, response, path):
        base_url = get_base_url(response)
        return urlparse.urljoin(base_url, path)

    def parse(self, response):
        print 'start crawling...'
        return self.parse_job_list_page(response)

    def parse_job_list_page(self, response):
        raise NotImplementedError('Must be overwritten')

    def parse_job_page(self, response):
        raise NotImplementedError('Must be overwritten')

    def _extract_common_tags(self, html_content):
        for tag in self.COMMON_TAGS:
            weight = html_content.count(tag)
            if weight:
                yield Tag(tag, weight)

    def extract_specific_tags(self, html_content):
        return []

    def extract_tags(self, html_content):
        html_content = html_content.lower()
        for tag in self._extract_common_tags(html_content):
            yield tag

        for tag in self.extract_specific_tags(html_content):
            yield tag
