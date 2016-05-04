#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import Queue
import threading

import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderMain(threading.Thread):
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
            print '>>> 1', page_url
            html_content = self.downloader.download(page_url)
            new_page_urls, new_question_urls = self.parser.parse_page(page_url, html_content)
            self.urls_mul.add_new_urls(new_page_urls, self.page_queue)
            self.urls_mul.add_new_urls(new_question_urls, self.question_queue)
            count += 1
            if count >= 10:
                break

        while not self.question_queue.empty():
            question_url = self.question_queue.get()
            print '>>> 2', question_url
            html_content = self.downloader.download(question_url)
            response_data = self.parser.parse_question(question_url, html_content)
            self.outputer.save_mysql(response_data)


if __name__ == '__main__':
    start_urls = ['https://segmentfault.com/t/java?type=votes',
                  'https://segmentfault.com/t/python?type=votes']
    # 队列
    page_queue = Queue.Queue()
    question_queue = Queue.Queue()
    data_queue = Queue.Queue()

    for url in start_urls:
        page_queue.put(url)

    threads = []
    thread_amount = 3

    for i in range(thread_amount):
        threads.append(SpiderMain(page_queue, question_queue, data_queue))

    for i in range(thread_amount):
        threads[i].start()

    for i in range(thread_amount):
        threads[i].join()
