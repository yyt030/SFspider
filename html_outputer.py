#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'
import config
import pymysql


class HtmlOutputer(object):
    def __init__(self):
        self.conn = pymysql.connect(host=config.mysql_host,
                                    user=config.mysql_user,
                                    password=config.mysql_password,
                                    db=config.mysql_db,
                                    charset=config.mysql_charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.sql_question = u'INSERT INTO question(title, view_num, create_time, author_id, vote_num, body_html, body) ' \
                            u'VALUES (%s, 0, current_timestamp, 1, 0, %s, %s)'
        self.sql_tag = u'insert into tag(name, category, create_time) ' \
                       u'values(%s, %s, current_timestamp)'
        self.sql_answer = u'insert into answer(title,create_time, author_id, vote_num,' \
                          u'question_id, body_html, body)' \
                          u'values ("", current_timestamp, 1,0, %s, %s, %s) '
        self.sql_question_tag = u'insert into question_tag (question_id, tag_id) values(%s, %s)'

    def save_mysql(self, data):
        if data is None or len(data) == 0:
            return
        value_args_question = unicode(data.get('question_title')), unicode(data.get('question_content')), unicode(
            data.get('question_content'))
        question_id = self._insert_record(self.sql_question, value_args_question)

        for tag in data.get('question_tags'):
            tag_id = self._insert_record(self.sql_tag, (tag, tag))
            if tag_id is None or question_id is None:
                continue
            self._insert_record(self.sql_question_tag, (question_id, tag_id))

        if question_id:
            for answer in data.get('answer_contents'):
                value_args_answer = question_id, unicode(answer), unicode(answer)
                self._insert_record(self.sql_answer, value_args_answer)

    def _insert_record(self, sql, value_args):
        if value_args is None or len(value_args) == 0:
            return
        last_row_id = None
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, value_args)
                last_row_id = cursor.lastrowid
            self.conn.commit()
            # print '>>>', __name__, 'insert into table on records'
        except pymysql.Error as e:
            print '>>>', e.args, e.message
            self.conn.rollback()
        return last_row_id

    def __del__(self):
        if self.conn:
            self.conn.close()
