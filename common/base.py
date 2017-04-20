#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import os
import datetime
import time
import pymongo
# import MySQLdb
import pymysql
from common.log.loger import my_log

class Config(object):
    def __init__(self, config_filename="cgss.conf"):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class MongoDb(object):
    def __init__(self, host, port, user=None, password=None):
        self._db_host = host
        self._db_port = int(port)
        self._user = user
        self._password = password
        self.conn = None

    def connect(self):
        self.conn = pymongo.MongoClient(self._db_host, self._db_port)
        return self.conn

    def get_db(self, db_name):
        collection = self.conn.get_database(db_name)
        if self._user and self._password:
            collection.authenticate(self._user, self._password)
        return collection

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


class My_Pymysql(object):
    """
    Parameters:

        -------
        connecta:
                pass

        run_manysql:
                pass

        select: fetch ("all", "one")

        close: pass


    Basic usage:
        ---------------------------------
        if __name__ == '__main__':

            ret = Config().get_content("sub_table")
            print(ret)
            ret = My_Pymysql(**ret)
            sql = "select * from `1111.sav`"
            ret.connecta()
            print ret.select(sql)
            ret.close()

        ----------------------------------

    """

    def __init__(self, host, port, user, password, db_name):
        self._db_host = host
        self._db_port = int(port)
        self._user = user
        self._password = str(password)
        self._db = db_name
        self.conn = None
        self.cursor = None
        # print [self._db_host,self._db_port, self._user, self._password, self._db]

    def connecta(self):
        self.conn = pymysql.connect(host=self._db_host, port=self._db_port, user=self._user, passwd=self._password,
                                    db=self._db,  charset="utf8")
        # self.conn.cursor()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def run_sql(self, sql):
        cursor = self.connecta()
        cursor.execute(sql)
        self.conn.commit()

    def run_manysql(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            my_log.error(e)
            return 5002
        my_log.info("sql执行语句成功; Sql execution statement is successful")
        return 2000

    def select_sql(self, sql, fetch="all"):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            if fetch == "all":
                return self.cursor.fetchall()
            elif fetch == "one":
                return self.cursor.fetchone()
        except Exception as e:
            my_log.error(e)
            return 5002

    def close(self):
        if self.conn:
            self.cursor = None
            self.conn.close()
            self.conn = None


def result(status, value):
    """
    staatus:
    2000, 什么都ok
    4000, 客户上传的文件格式不正确
    4001， 客户上传的文件列超过5400
    4002， 暂时梅想到
    5000， 服务器错误
    5001， 数据表已经存在
    5002,  sql语句错误
    """
    if status == 2000:
        message = u"True"
    elif status == 4000:
        message = u"客户上传的文件格式不正确"
    elif status == 4001:
        message = u"客户上传的文件列超过5400"
    elif status == 4002:
        message = u"暂时梅想到"
    elif status == 5000:
        message = u"服务器错误"
    elif status == 5001:
        message = u"数据表已经存在"
    elif status == 5002:
        message = u"sql语句错误"
    else:
        message = u"未知错误"
    return {
        "statuscode": status,
        "statusmessage": message,
        "value": value
    }


class my_datetime():
    """
    Basic usage:

        a = datetime.datetime(2016, 9, 21, 13, 42, 8)
        b = "2016-11-15 15:32:12"
        c = u'2016-09-21 13:37:34'
        print type(c)
        d = 1474436826.0
        e = 13710788676.0
        ret = my_datetime()
        res = ret.become_datetime(e)
        print res
        print type(res)
    """

    def __init__(self):
        # 缺少对utc时间的判断
        pass

    def become_timestamp(self, dtdt):
        # 将时间类型转换成时间戳
        if isinstance(dtdt, datetime.datetime):
            timestamp = time.mktime(dtdt.timetuple())
            return timestamp

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d  %H:%M:%S")
                timestamp = time.mktime(a_datetime.timetuple())
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                timestamp = time.mktime(a_datetime.timetuple())
            return timestamp

        elif isinstance(dtdt, float):
            return dtdt

        elif isinstance(dtdt, unicode):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
                timestamp = time.mktime(a_datetime.timetuple())
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                timestamp = time.mktime(a_datetime.timetuple())
            return timestamp

    def become_datetime(self, dtdt):
        # 将时间类型转换成datetime类型
        if isinstance(dtdt, datetime.datetime):
            return dtdt

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            return a_datetime

        elif isinstance(dtdt, float):
            # 把时间戳转换成datetime类型
            a_datetime = datetime.datetime.fromtimestamp(dtdt)
            return a_datetime

        elif isinstance(dtdt, unicode):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            return a_datetime

    def become_str(self, dtdt):
        # 把时间类型转换成字符串
        if isinstance(dtdt, datetime.datetime):
            a_datetime = dtdt.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

        elif isinstance(dtdt, str):
            return dtdt

        elif isinstance(dtdt, float):
            a_datetime_local = datetime.datetime.fromtimestamp(dtdt)
            a_datetime = a_datetime_local.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

        elif isinstance(dtdt, unicode):
            # 区别：一个是strp， 一个是strf
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
                a_datetime = a_datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                a_datetime = a_datetime.strftime("%Y-%m-%d")
            return a_datetime

if __name__ == '__main__':
    print(my_datetime().become_str(13693844826.0))