#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import Queue
import datetime
import threading

import config
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
    current_page_number = 0
    current_url_number = 0
    lock = threading.RLock()

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.in_queue = queue

        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def run(self):
        while True:
            try:
                type, url_or_data = self.in_queue.get(block=False, timeout=1)
            except Queue.Empty:
                # 队列任务都消费完且已达到限制条件
                if SpiderByQueue.current_page_number > config.page_number:
                    break
            else:
                if type == 'page_url':
                    print '>>> {} page_url:{}'.format(self.getName(), url_or_data)
                    html_content = self.downloader.download(url_or_data)
                    new_page_urls, new_question_urls = self.parser.parse_page(url_or_data, html_content)

                    for new_page_url in new_page_urls:
                        self.in_queue.put(['page_url', new_page_url])
                    for new_question_url in new_question_urls:
                        self.in_queue.put(['question_url', new_question_url])

                    with SpiderByQueue.lock:
                        SpiderByQueue.current_page_number += len(new_page_urls)
                        SpiderByQueue.current_url_number += len(new_page_urls) + len(new_question_urls)


                elif type == 'question_url':
                    print '>>> {} question_url:{}'.format(self.getName(), url_or_data)
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

    # 放入初始url
    for url in start_urls:
        url_or_data_queue.put(['page_url', url])

    # 线程启动哦
    start_time = datetime.datetime.now()
    thread_download_amount = config.concurrent_thread_amount or 10
    threads = [SpiderByQueue(url_or_data_queue) for _ in xrange(thread_download_amount)]

    for thread in threads:
        thread.setDaemon(True)
        thread.start()

    # 线程同步
    for thread in threads:
        thread.join()

    print '{}\nTotal pages:{}, urls:{}, times:{}'.format('*' * 30, SpiderByQueue.current_page_number,
                                                         SpiderByQueue.current_url_number,
                                                         datetime.datetime.now() - start_time)
