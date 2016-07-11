#!/usr/bin/env python
# encoding: utf-8

__author__ = 'yueyt'

from urllib.parse import urljoin

import requests

import config


class HtmlDownloader(object):
    def __init__(self):
        self.headers = config.request_header
        self.s = requests.session()
        self.s.headers = config.request_header
        self.s.post(config.login_url, data=config.login_post_data)

    # post downloader
    def post_downloader(self, type, req_data):
        processor = config.processor.get(type)
        if not processor:
            print("i can't get processor", __name__, type, req_data)
            return
        url = urljoin(config.root_url, processor.get('url'))
        payload = processor.get('payload')
        # dict
        if req_data:
            payload.update(req_data)
        r = self.s.post(url, data=payload)
        # debug
        if type == 'loaninfo_detail_downloader':
            print('>>>', payload)
        return r.content

    # get downloader
    def get_downloader(self, type, url):
        processor = config.processor.get(type)
        if not processor:
            print("i can't get processor", __name__, type, url)
            return
        url = urljoin(config.root_url, url)
        print('U' * 10, url)
        r = self.s.get(url)
        return r.content
