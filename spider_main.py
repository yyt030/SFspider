#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import Queue
import datetime
import random
import threading

import config
import html_downloader
import html_outputer
import html_parser


class SpiderByQueue(threading.Thread):
    current_url_number = 0
    lock = threading.RLock()

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.in_queue = queue

        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.zhihu_parser = html_parser.ZhihuParser()
        self.outputer = html_outputer.HtmlOutputer()

        # 定义函数对照表,主要解决解析函数过多，类型过多的问题
        self.function_table = {
            # 类型: 解析实例.解析函数
            ## Zhihu
            'topic_url': self.zhihu_parser.parse_subtopic,
            'subtopic_url': self.zhihu_parser.parse_top_question_url,
            'answer_url': self.zhihu_parser.parse_question_detail,
            ## SegmentFault
            'page_url': self.parser.parse_page,
            'question_url': self.parser.parse_question,

            'data': self.outputer.save_mysql
        }

    def run(self):
        while True:
            try:
                type, url_or_data = self.in_queue.get(block=False, timeout=1)
            except Queue.Empty:
                # 队列任务都消费完且已达到限制条件
                if SpiderByQueue.current_url_number > config.url_number:
                    break
            else:
                func = self.function_table.get(type)  # 解析报文函数
                if not func:
                    print('::: not found right function:', type, url_or_data)
                    continue

                if type == 'data':
                    func(url_or_data)
                else:
                    print '>>>', self.getName(), type, url_or_data
                    html_content = self.downloader.download(url_or_data)
                    # 解析函数, 返回list, 每项类型为tuple
                    response_data = func(url_or_data, html_content)
                    if response_data is None or len(response_data) == 0:
                        continue

                    with SpiderByQueue.lock:
                        if type in ['topic_url',
                                    'subtopic_url'] and SpiderByQueue.current_url_number > config.url_number:
                            continue

                        if str(type).endswith('url'):
                            SpiderByQueue.current_url_number += len(response_data)
                    try:
                        for next_type, data in response_data:
                            self.in_queue.put([next_type, data])
                    except TypeError:
                        print 'ERROR:', response_data


def main():
    # 开始爬取的urls
    start_urls = config.start_urls
    # 队列
    url_or_data_queue = Queue.Queue()

    # 放入初始url
    for url in start_urls:
        url_or_data_queue.put(['topic_url', url])

    # 线程启动哦
    start_time = datetime.datetime.now()
    thread_download_amount = config.concurrent_thread_amount or 10
    threads = [SpiderByQueue(url_or_data_queue) for _ in range(thread_download_amount)]

    for thread in threads:
        thread.setDaemon(True)
        thread.start()

    # 线程同步
    for thread in threads:
        thread.join()

    print('{}\nTotal urls: {}, times:{}'.format('*' * 30, SpiderByQueue.current_url_number,
                                                datetime.datetime.now() - start_time))


### Main function
if __name__ == '__main__':
    main()
