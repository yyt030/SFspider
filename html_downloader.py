#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import time

import requests


class HtmlDownloader(object):
    def __init__(self):
        self.headers = {
            'Host': 'segmentfault.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,en-US;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Cache-Control': "no-cache",
            'Pragma': "no-cache"
        }

    def download(self, url):
        if url is None:
            return None
        try:
            r = requests.get(url, headers=self.headers)
            time.sleep(1)
        except requests.ConnectionError as e:
            print '>>>', url, e.args, e.message,
            return None
        else:
            if r.status_code != 200:
                return None
            return r.content
