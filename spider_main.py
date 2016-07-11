#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

from queue import Queue, Empty
import datetime
import threading

import config
from html_downloader import HtmlDownloader
from html_parser import CreditParser
from html_outputer import HtmlOutputer


class SpiderByQueue(threading.Thread):
    current_url_number = 0

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.download = HtmlDownloader()
        self.parser = CreditParser(queue)
        self.output = HtmlOutputer()

    def get_processer(self, type, *args):
        """
            主要处理逻辑函数，根据配置文件，获取执行逻辑处理的先后顺序
        """
        is_found = False
        object_list = [self.download, self.parser, self.output]
        for obj in object_list:
            try:
                # 根据当前的type 获取当前数据的解析函数
                f = getattr(obj, config.processor.get(type).get('function'))
            except AttributeError as e:
                # print(e.args, e)
                pass
            else:
                is_found = True
                # print(f)
                # 执行当前函数并将处理结果返回，供后续处理
                result = f(type, *args)
                if result:
                    self.queue.put([config.processor.get(type).get('next_processor'), result])
        if not is_found:
            print(">>> ERROR: i can't found the processor:", type, *args)

    def run(self):
        while True:
            try:
                type, *args = self.queue.get(block=False, timeout=1)
                self.get_processer(type, *args)
            except Empty:
                print(">>> ERROR: queue empty")
                break


def main():
    # queue
    url_or_data_queue = Queue()

    # 放入初始url
    start_point = 'orgcodeinfo_downloader'
    req_data = dict(corpno='10000349-5')
    url_or_data_queue.put([start_point, req_data])

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
