# SFspider
##整体说明
本工程是爬虫框架, 爬取SF网站的问题以及应答，并插入MySQL db中

##工程文件
* url_manager.py
 URL 管理器
* html_downloader.py
 下载器
* html_parser.py
 解析器
* html_outputer.py
 输出器
* init.sql
初始化SQL

##配置参数
* 并发线程数
concurrent_thread_amount = 10
* 爬取下载延迟
download_delay = 1
* 爬取前几页
page_num = 10
* 定义函数对照表,主要解决解析函数过多，类型过多的问题
self.function_table = {...}

## 使用
* 执行init.sql 建表
* 配置config.py的start_urls
* 修改spider_main.py的“放入初始url”部分
* 编辑self.function_table映射表
* 修改解析函数逻辑解析

## TODO
* redis使用: 使用redis管理url,并实现分布式爬取


