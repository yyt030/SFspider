#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import urlparse

import re
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self):
        pass

    def _get_new_page_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', rel='next', href=re.compile(r'/\w'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_question_urls(self, page_url, soup):
        new_question_urls = set()
        links = soup.find_all('a', href=re.compile(r'/q/'))
        for link in links:
            new_full_question_url = urlparse.urljoin(page_url, link['href'])
            new_question_urls.add(new_full_question_url)
        return new_question_urls

    def _get_new_detail_data(self, page_url, soup):
        response_data = {}
        response_data['url'] = page_url
        question_title = soup.find('h1', id='questionTitle')
        question_content = soup.find('div', class_='question fmt')
        question_id = question_content.attrs.get('data-id')
        answer_contents = soup.find_all('div', class_='answer fmt')
        # print '>>>', type(answer_contents)
        response_data['answer_contents'] = []
        for content in answer_contents:
            response_data['answer_contents'].append([child for child in content.children])

        response_data['question_title'] = question_title.a.string
        response_data['question_id'] = question_id
        response_data['question_content'] = question_content

        print '>>>', response_data
        return response_data

    def parse(self, page_url, html_content):
        if page_url is None or html_content is None:
            return None
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        new_page_urls = self._get_new_page_urls(page_url, soup)
        new_question_urls = self._get_new_question_urls(page_url, soup)
        return new_page_urls, new_question_urls

    def parse_question(self, question_url, html_content):
        if question_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        self._get_new_detail_data(question_url, soup)
        return
