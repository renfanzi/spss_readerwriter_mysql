#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import MySQLdb
import json
from common.base import Config, My_Pymysql
from common.log.loger import my_log
from models.base import base_model


def create_data_table(vartypes, width, valuetypes, formats, varnames, filename, libname="data"):
    sql = """CREATE TABLE `{}` (""".format(filename)
    for i in range(len(varnames)):
        if valuetypes[i] == "FLOAT":
            num = width[i].split(".")
            s = "`{}` {}({},{}) DEFAULT NULL".format(varnames[i], valuetypes[i], num[0], num[1])
        elif valuetypes[i] == "DATETIME":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "DATE":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "VARCHAR":
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], str(int(width[i])+10))
        else:
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], width[i])

        if i < len(varnames) - 1:
            sql = sql + s + ","
        elif i == len(varnames) - 1:
            sql = sql + s

    sql = sql + ") ENGINE=InnoDB DEFAULT CHARSET=UTF8"
    res = base_model(libname).connect()
    res.adu_sql(sql)
    res.close()


class writer_data_table():
    def __init__(self, libname="data"):
        self.libname= libname
        self.res = base_model(libname).connect()

    def insert_sql(self, tablename, data):
        data = tuple(data)
        sql = "insert INTO `{}` VALUES {};".format(tablename, data)
        self.res.adu_sql(sql)

    def close(self):
        self.res.close()


def create_information_tables(tablename, libname="information"):
    sql = """CREATE TABLE `{}` (
            `name` VARCHAR (255) DEFAULT NULL,
            `type` VARCHAR (255) DEFAULT NULL,
            `width` INT (5) DEFAULT NULL,
            `float_width` INT (5) DEFAULT NULL,
            `varlabels` text DEFAULT NULL,
            `valuelabels` text DEFAULT NULL,
            `formats` VARCHAR(255) DEFAULT NULL,
            `missing_value` VARCHAR(255) DEFAULT NULL,
            `theme` VARCHAR(255) DEFAULT NULL
            ) ENGINE = INNODB DEFAULT CHARSET = utf8;""".format(tablename)
    res = base_model(libname).connect()
    res.adu_sql(sql)
    res.close()


class writer_information_tables():
    def __init__(self, libname="information"):
        self.libname= libname
        self.res = base_model(libname).connect()

    def insert_sql(self, tablename, data):
        data = tuple(data)
        sql = "insert INTO `{}` VALUES {}".format(tablename, data)
        self.res.adu_sql(sql)

    def close(self):
        self.res.close()



if __name__ == '__main__':
    # ret = create_tables()

    # res = writer_tables()
    # res.conn()
    # res.run_sql("222", ['hrYjT71474436254', '2016-09-21 13:37:34'])
    # res.close()
    pass
