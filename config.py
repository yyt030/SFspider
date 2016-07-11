#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

import request_payload

# 爬取数据的存储位置 mysql
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'root'
mysql_db = 'answers'
mysql_charset = 'utf8'

# 下载器使用的request header
request_header = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


# 并发线程数
concurrent_thread_amount = 1

# base root url
root_url = ''
# 登录网站的首页
login_url = root_url + 'logon.do'
login_post_data = {
    'orgCode': '',
    'userid': '',
    'password': ''
}

# 处理流程配置表:页面下载器(downloader),下载器(parser),  数据保存器（saver）
processor = {
    'orgcodeinfo_downloader': {
        'function': 'post_downloader',
        'url': 'newConfirmEditQuery.do',
        'payload': request_payload.credit_search_payload,
        'next_processor': 'orgcodeinfo_parser',
    },
    'orgcodeinfo_parser': {
        'function': 'orgcodeinfo_parser',
        'detail_point': 'loaninfo_list_downloader',
        'next_processor': 'saver'
    },
    # list 页面
    'loaninfo_list_downloader': {
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': request_payload.loaninfo_list_payload,
        'next_processor': 'loaninfo_list_parser'
    },
    'loaninfo_list_parser': {
        'function': 'loaninfo_list_parser',
        'detail_point': 'loaninfo_detail_downloader',
        'next_processor': 'saver'
    },
    # detail
    'loaninfo_detail_downloader': {
        'function': 'get_downloader',
        'next_processor': 'loaninfo_detail_parser'
    },
    'loaninfo_detail_parser': {
        'function': 'loaninfo_detail_parser',
        'next_processor': 'saver'
    },

    'saver': {
        'function': 'save_record',
        'next_processor': '',
    }
}
