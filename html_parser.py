#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

from bs4 import BeautifulSoup

import request_payload
import config


class CreditParser(object):
    def __init__(self, queue):
        self.queue = queue

    def orgcodeinfo_parser(self, type, page):
        """ 信息服务>> 确定借款人"""
        result_list = []
        column_number = len(request_payload.credit_list_title)
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        records = soup.select('table#list tr')
        for record in records:
            row = []
            columns = record.select('td')
            if not columns:
                continue
            for column in columns:
                if column.findChild():
                    values = column.select_one('a > font')
                    if values:
                        row.append(values.string.strip())
                else:
                    row.append(column.string.strip())
            # 过滤不完整的记录
            if len(row) < column_number:
                continue
            rec_dict = dict(zip(request_payload.credit_list_title, row))
            result_list.append(rec_dict)

            # 根据中征码 点击查询“贷款余额”,
            detail_point = config.processor.get(type).get('detail_point')
            if detail_point:
                payload = dict(
                    loancard=rec_dict.get('midsigncode')
                )
                self.queue.put([detail_point, payload])
        return result_list

    def loaninfo_list_parser(self, type, page):
        """信息查询>>借款人信用报告明细查询>>余额详细信息>>贷款余额"""
        result_list = []
        column_number = len(request_payload.loaninfo_list_title)
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        records = soup.select('table#list tr')
        for record in records:
            row = []
            detail_url = ''
            columns = record.select('td')
            if not columns:
                continue
            for column in columns:
                if column.findChild():
                    values = column.select_one('a > font')
                    if values:
                        row.append(values.string.strip())
                    detail_url_tag = column.select_one('a[href]')
                    if detail_url_tag:
                        detail_url = detail_url_tag.get('href')
                else:
                    row.append(column.string.strip())
            # 过滤不完整的记录
            if len(row) < column_number:
                continue
            rec_dict = dict(zip(request_payload.loaninfo_list_title, row))
            result_list.append(rec_dict)

            # 根据合同号码 点击查询“贷款合同信息”,
            detail_point = config.processor.get(type).get('detail_point')
            if detail_point and detail_url:
                self.queue.put([detail_point, detail_url])
        return result_list

    def loaninfo_detail_parser(self, type, page):
        """信息查询>>借款人信用报告明细查询>>余额详细信息>>贷款余额 >> 贷款合同信息"""
        result_list = []
        column_number = len(request_payload.loaninfo_list_title)
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        records = soup.select('table#list > tbody > tr > td')
        loaninfo_detail = [record.string for n, record in enumerate(records) if n % 2 == 0]
        print('>>>', )


        # for record in records:
        #     row = []
        #     columns = record.select('td')
        #     if not columns:
        #         continue
        #     for column in columns:
        #         if column.findChild():
        #             values = column.select_one('a > font')
        #             if values:
        #                 row.append(values.string.strip())
        #         else:
        #             row.append(column.string.strip())
        #     # 过滤不完整的记录
        #     if len(row) < column_number:
        #         continue
        #     rec_dict = dict(zip(request_payload.loaninfo_list_title, row))
        #     result_list.append(rec_dict)
        #
        #     # 根据合同号码 点击查询“贷款合同信息”,
        #     detail_point = config.processor.get(type).get('detail_point')
        #     if detail_point:
        #         payload = dict(
        #             loancard=rec_dict.get('contractnumber')
        #         )
        #         self.queue.put([detail_point, payload])
        return result_list


if __name__ == '__main__':
    with open('html_demo/balance.html', encoding='gbk') as f:
        page = f.read()
        soup = BeautifulSoup(page, 'html.parser', from_encoding='utf-8')
        records = soup.select('table#list tr')
