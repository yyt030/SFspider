#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'


class UrlManager(object):
    """URL 管理器"""

    def __init__(self):
        self.new_page_urls = set()
        self.new_question_urls = set()
        self.new_answer_urls = set()
        self.old_urls = set()

    def add_new_url(self, url, type='page'):
        if url is None:
            return
        if type == 'page':
            if url not in self.new_page_urls and url not in self.old_urls:
                self.new_page_urls.add(url)
        if type == 'question':
            if url not in self.new_question_urls and url not in self.old_urls:
                self.new_question_urls.add(url)
        if type == 'answer':
            if url not in self.new_answer_urls and url not in self.old_urls:
                self.new_answer_urls.add(url)

    def add_new_urls(self, urls, type='page'):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url, type)

    def has_new_url(self, type='page'):
        if type == 'page':
            return len(self.new_page_urls) != 0
        if type == 'question':
            return len(self.new_question_urls) != 0
        if type == 'answer':
            return len(self.new_answer_urls) != 0
        return None

    def get_new_url(self, type='page'):
        new_url = ''
        if type == 'page':
            new_url = self.new_page_urls.pop()
        if type == 'question':
            new_url = self.new_question_urls.pop()
        if type == 'answer':
            new_url = self.new_answer_urls.pop()
        self.old_urls.add(new_url)
        return new_url
