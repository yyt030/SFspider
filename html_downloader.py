#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import time

import config
import requests


class HtmlDownloader(object):
    def __init__(self):
        self.headers = config.request_header

    def download(self, url):
        if url is None:
            return None
        try:
            r = requests.get(url, headers=self.headers)
            time.sleep(config.download_delay or 1)
        except requests.ConnectionError as e:
            print '>>>', url, e.args, e.message,
            return None
        else:
            if r.status_code != 200:
                return None
            return r.content
