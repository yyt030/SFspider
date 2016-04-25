#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderMain(object):
    def __init__(self):
        # url管理器
        self.urls = url_manager.UrlManager()
        # 下载器
        self.downloader = html_downloader.HtmlDownloader()
        # 解析器
        self.parser = html_parser.HtmlParser()
        # 输出器
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        page_number = 1
        self.urls.add_new_url(root_url)
        try:
            while self.urls.has_new_url():
                new_url = self.urls.get_new_url()
                html_content = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_content)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if page_number >= 1:
                    break
                page_number += 1
        except Exception as e:
            print 'craw failed:{}{}', e.args, e.message

        self.outputer.output_html()


if __name__ == '__main__':
    root_url = 'https://segmentfault.com/t/python?type=votes'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
