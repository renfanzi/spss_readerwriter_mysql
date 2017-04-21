#!/usr/bin/env python
# -*- coding:utf-8 -*-
from common.base import Config, My_Pymysql
from common.base import my_log
class base_model():
    """
    #Basic usage:

        ------------------------------
        if __name__ == '__main__':
            sql = "select * from `2111.sav`"
            res = base_model('sub_table')
            res.connect()
            query_result = res.select_sql(sql)
            print query_result
            res.close()
        **************************************
            res = base_model(libname).connect()
            res.adu_sql(sql)
            res.close()
        ------------------------------

    """
    def __init__(self, conf_name):
        self.conf = Config().get_content(conf_name)
        self.conn = None

    def connect(self):
        self.conn = My_Pymysql(**self.conf)
        self.conn.connecta()
        return self

    def adu_sql(self, sql):
        # adu: insert, delete, update的简写
        try:
            self.conn.run_manysql(sql)
        except Exception as e:
            my_log.error(e)
            return
        return 2000

    def insert_sql(self, sql, value):
        # adu: insert, delete, update的简写
        try:
            lastrowid = self.conn.insert_sql(sql, value)
        except Exception as e:
            my_log.error(e)
            return
        return lastrowid

    def select_sql(self, sql):
        try:
            query_result = self.conn.select_sql(sql)
        except Exception as e:
            my_log.error(e)
            return
        return query_result

    def close(self):
        self.conn.close()
        self.conn = None