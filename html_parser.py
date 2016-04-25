#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import urlparse

import re
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self):
        pass

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', rel='next', href=re.compile(r'/\w'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url


        return res_data

    def parse(self, page_url, html_content):
        if page_url is None or html_content is None:
            return None
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
