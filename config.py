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
    'Host': 'www.zhihu.com',
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
page_number = 2

# start url
start_urls = [u'https://www.zhihu.com/topics#\u6e38\u620f', u'https://www.zhihu.com/topics#\u8fd0\u52a8',
              u'https://www.zhihu.com/topics#\u4e92\u8054\u7f51', u'https://www.zhihu.com/topics#\u827a\u672f',
              u'https://www.zhihu.com/topics#\u9605\u8bfb', u'https://www.zhihu.com/topics#\u7f8e\u98df',
              u'https://www.zhihu.com/topics#\u52a8\u6f2b', u'https://www.zhihu.com/topics#\u6c7d\u8f66',
              u'https://www.zhihu.com/topics#\u751f\u6d3b\u65b9\u5f0f',
              u'https://www.zhihu.com/topics#\u6559\u80b2', u'https://www.zhihu.com/topics#\u6444\u5f71',
              u'https://www.zhihu.com/topics#\u5386\u53f2', u'https://www.zhihu.com/topics#\u6587\u5316',
              u'https://www.zhihu.com/topics#\u65c5\u884c',
              u'https://www.zhihu.com/topics#\u804c\u4e1a\u53d1\u5c55',
              u'https://www.zhihu.com/topics#\u7ecf\u6d4e\u5b66', u'https://www.zhihu.com/topics#\u8db3\u7403',
              u'https://www.zhihu.com/topics#\u7bee\u7403', u'https://www.zhihu.com/topics#\u6295\u8d44',
              u'https://www.zhihu.com/topics#\u97f3\u4e50', u'https://www.zhihu.com/topics#\u7535\u5f71',
              u'https://www.zhihu.com/topics#\u6cd5\u5f8b',
              u'https://www.zhihu.com/topics#\u81ea\u7136\u79d1\u5b66',
              u'https://www.zhihu.com/topics#\u8bbe\u8ba1', u'https://www.zhihu.com/topics#\u521b\u4e1a',
              u'https://www.zhihu.com/topics#\u5065\u5eb7', u'https://www.zhihu.com/topics#\u5546\u4e1a',
              u'https://www.zhihu.com/topics#\u4f53\u80b2', u'https://www.zhihu.com/topics#\u79d1\u6280',
              u'https://www.zhihu.com/topics#\u5316\u5b66', u'https://www.zhihu.com/topics#\u7269\u7406\u5b66',
              u'https://www.zhihu.com/topics#\u751f\u7269\u5b66', u'https://www.zhihu.com/topics#\u91d1\u878d'
              ]
