#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import sys
from urlparse import urljoin

import re
from bs4 import BeautifulSoup

sys.setrecursionlimit(10000)


class HtmlParser(object):
    def __init__(self):
        pass

    def _get_new_page_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', rel='next', href=re.compile(r'/\w'))
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_question_urls(self, page_url, soup):
        new_question_urls = set()
        links = soup.find_all('a', href=re.compile(r'/q/'))
        for link in links:
            new_full_question_url = urljoin(page_url, link['href'])
            new_question_urls.add(new_full_question_url)
        return new_question_urls

    def _get_new_detail_data(self, page_url, soup):
        response_data = {}
        response_data['url'] = page_url
        question_title = soup.find('h1', id='questionTitle')
        question_content = soup.find('div', class_='question fmt')
        question_id = question_content.attrs.get('data-id')
        question_tags = soup.find_all('a', class_='tag', href=re.compile(r'/t/'))
        answer_contents = soup.find_all('div', class_='answer fmt')

        response_data['answer_contents'] = []
        for content in answer_contents:
            response_data['answer_contents'].append(''.join(map(unicode, [child for child in content.children])))

        response_data['question_title'] = question_title.a.string
        response_data['question_id'] = question_id
        response_data['question_content'] = question_content
        response_data['question_tags'] = [tag.string for tag in question_tags]

        return response_data

    def parse_page(self, page_url, html_content):
        if page_url is None or html_content is None:
            return set(), set()
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        new_page_urls = self._get_new_page_urls(page_url, soup)
        new_question_urls = self._get_new_question_urls(page_url, soup)
        return new_page_urls, new_question_urls

    def parse_question(self, question_url, html_content):
        if question_url is None or html_content is None:
            return None
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        new_data = self._get_new_detail_data(question_url, soup)
        return new_data


class ZhihuParser:
    def __init__(self):
        pass

    def parse_subtopic(self, base_url, html_content):
        if base_url is None or html_content is None:
            return set(), set()
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        topics = soup.find_all(class_='blk')
        subtopic_urls = [urljoin(base_url, '{}/top-answers'.format(topic.a.get('href'))) for topic in topics]
        return subtopic_urls

    def parse_topic_question_url(self, base_url, html_content):
        if html_content is None:
            return set(), set()
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        next_subtopic_urls = soup.find(href=re.compile(r'page='), text=u'下一页')
        if next_subtopic_urls:
            next_subtopic_urls = [urljoin(base_url, next_subtopic_urls.get('href'))]
        new_question_urls = soup.find_all(class_='question_link')
        if new_question_urls:
            new_question_urls = [urljoin(base_url, b.get('href')) for b in new_question_urls]

        return next_subtopic_urls, new_question_urls

    def parse_question_detail(self, url, html_content):
        if url is None or html_content is None:
            return None
        response_data = {}
        response_data['url'] = url

        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
        question_title = soup.find('h2', class_='zm-item-title zm-editable-content')
        if question_title:
            response_data['question_title'] = question_title.string.strip()
        question_content = soup.find('div', id='zh-question-detail')
        response_data['question_content'] = ''.join([unicode(i).strip() for i in question_content.div])
        response_data['question_id'] = url
        response_data['question_tags'] = [unicode(tag.string).strip() for tag in
                                          soup.find_all('a', class_='zm-item-tag')]

        response_data['answer_contents'] = []
        answer_contents = soup.find_all('div', class_='zm-editable-content clearfix')
        for answer_content in answer_contents:
            response_data['answer_contents'].append(''.join([unicode(i).strip() for i in answer_content.children]))

        return response_data
