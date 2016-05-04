#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import Queue
import threading

import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderByUrl(threading.Thread):
    def __init__(self, page_queue, question_queue, data_queue):
        threading.Thread.__init__(self)
        self.page_queue = page_queue
        self.question_queue = question_queue
        self.data_queue = data_queue

        # url管理器
        self.urls_mul = url_manager.UrlManagerMul()
        # 下载器
        self.downloader = html_downloader.HtmlDownloader()
        # 解析器
        self.parser = html_parser.HtmlParser()
        # 输出器
        self.outputer = html_outputer.HtmlOutputer()

    def crawler(self, root_urls):
        page_number = 1
        self.urls.add_new_urls(root_urls, type='page')
        try:
            while self.urls.has_new_url('page'):
                next_page_url = self.urls.get_new_url('page')
                html_content = self.downloader.download(next_page_url)
                new_page_urls, new_question_urls = self.parser.parse_page(next_page_url, html_content)
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

    def run(self):
        count = 1
        while not self.page_queue.empty():
            page_url = self.page_queue.get()
            html_content = self.downloader.download(page_url)
            new_page_urls, new_question_urls = self.parser.parse_page(page_url, html_content)
            self.urls_mul.add_new_urls(new_page_urls, self.page_queue)
            self.urls_mul.add_new_urls(new_question_urls, self.question_queue)
            count += 1
            if count >= 10:
                break

        while not self.question_queue.empty():
            question_url = self.question_queue.get()
            html_content = self.downloader.download(question_url)
            response_data = self.parser.parse_question(question_url, html_content)
            self.outputer.save_mysql(response_data)


class SpiderByQueue(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.in_queue = queue

        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def run(self):
        page_num = 0
        while True:
            type, url_or_data = self.in_queue.get()
            if type == 'page_url':
                print '>>>', self.getName(), type, url_or_data
                html_content = self.downloader.download(url_or_data)
                new_page_urls, new_question_urls = self.parser.parse_page(url_or_data, html_content)
                for new_page_url in new_page_urls:
                    self.in_queue.put(['page_url', new_page_url])
                for new_question_url in new_question_urls:
                    self.in_queue.put(['question_url', new_question_url])

                # 限制爬取页数
                page_num += 1
                if page_num > 10:
                    if self.in_queue.empty():
                        break
                    continue
            elif type == 'question_url':
                print '>>>', self.getName(), type, url_or_data
                html_content = self.downloader.download(url_or_data)
                response_data = self.parser.parse_question(url_or_data, html_content)
                if response_data is None or len(response_data) == 0:
                    continue
                self.in_queue.put(['data', response_data])
            elif type == 'data':
                self.outputer.save_mysql(url_or_data)


if __name__ == '__main__':
    start_urls = ['https://segmentfault.com/t/java?type=votes',
                  'https://segmentfault.com/t/python?type=votes']
    # 队列
    url_or_data_queue = Queue.Queue()
    data_queue = Queue.Queue()

    for url in start_urls:
        url_or_data_queue.put(['page_url', url])

    threads = []
    thread_download_amount = 10

    for i in range(thread_download_amount):
        threads.append(SpiderByQueue(url_or_data_queue))

    for i in range(thread_download_amount):
        threads[i].start()

    for i in range(thread_download_amount):
        threads[i].join()

    data_queue.join()
    print 'all done'
