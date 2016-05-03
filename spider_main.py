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

    def craw(self, root_urls):
        page_number = 1
        self.urls.add_new_urls(root_urls, type='page')
        try:
            while self.urls.has_new_url('page'):
                next_page_url = self.urls.get_new_url('page')
                html_content = self.downloader.download(next_page_url)
                new_page_urls, new_question_urls = self.parser.parse(next_page_url, html_content)
                self.urls.add_new_urls(new_page_urls, type='page')
                self.urls.add_new_urls(new_question_urls, type='question')

                # 问题详情含具体的回答内容
                while self.urls.has_new_url('question'):
                    question_url = self.urls.get_new_url('question')
                    html_content = self.downloader.download(question_url)
                    response_data = self.parser.parse_question(question_url, html_content)
                    self.outputer.save_mysql(response_data)

                if page_number >= 10:
                    break
                page_number += 1
        except Exception as e:
            print 'craw failed:{}{}'.format(e.args, e.message)


if __name__ == '__main__':
    root_urls = ['https://segmentfault.com/t/java?type=votes']
    #root_url = 'https://segmentfault.com/t/python'
    obj_spider = SpiderMain()
    obj_spider.craw(root_urls)
