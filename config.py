#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

# 爬取数据的存储位置 mysql
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'root'
mysql_db = 'answers'
mysql_charset = 'utf8'

# 下载器使用的request header
request_header = {
    #'Host': 'www.zhihu.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,en-US;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Cache-Control': "max-age=0",
    'Pragma': "no-cache"
}

# 并发线程数
concurrent_thread_amount = 10

# 爬取下载延迟
download_delay = 1

# 爬取前几页
url_number = 10

# start url
start_urls = [
    'https://segmentfault.com/t/python',
]
