#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import MySQLdb
import json
import datetime
from common.base import Config, My_Pymysql
from common.base import my_log
from models.base import base_model


def create_data_table(vartypes, width, valuetypes, formats, varnames, tablename, libname="data"):

    sql = """CREATE TABLE `{}` (""".format(tablename)
    for i in range(len(varnames)):
        if valuetypes[i] == "FLOAT":
            num = width[i].split(".")
            s = "`{}` {}({},{}) DEFAULT NULL".format(varnames[i], valuetypes[i], num[0], num[1])
        elif valuetypes[i] == "DATETIME":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "DATE":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "VARCHAR":
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], width[i])
        else:
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], width[i])

        if i < len(varnames) - 1:
            sql = sql + s + ","
        elif i == len(varnames) - 1:
            sql = sql + s

    sql = sql + ") ENGINE=InnoDB DEFAULT CHARSET=UTF8"

    res = base_model(libname).connect()

    res.adu_sql("""DROP TABLE IF EXISTS {}""".format(tablename))
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
    def __init__(self, libname="user_information"):
        self.libname= libname
        self.res = base_model(libname).connect()

    def insert_sql(self, tablename, data):
        data = tuple(data)
        sql = "insert INTO `data_information` VALUES {};".format(data)
        self.res.adu_sql(sql)

    def close(self):
        self.res.close()


class insert_project_infor():
    def __init__(self, libname="user_information"):
        self.libname= libname
        self.res = base_model(libname).connect()
        # user_table, proj_table, dataset_table, datainfor_table
        self.table = Config().get_content("user_proj")

    # 插入 project表的信息
    def insert_project(self, user_id, proj_name):
        # proj_id, user_id, proj_name
        sql, value = "insert INTO project SET user_id=%s, proj_name=%s", ( user_id, proj_name)
        lastrowid = self.res.insert_sql(sql, value)
        return lastrowid

    # project_id
    def select_project_id(self, user_id, proj_name):
        # proj_id, user_id, proj_name
        sql = "select proj_id from `project` where user_id={} and proj_name='{}';".format(user_id, proj_name)
        project_id = self.res.select_sql(sql)
        return project_id

    # 插入 dataset表的信息
    def insert_dataset(self, dataset_id, proj_id, dataset_name, datatable_name, origin_filepath, origin_filetype):
        # dataset_id, proj_id, dataset_name, datatable_name, origin_filepath, origin_filetype
        sql = "insert INTO `dataset` SET dataset_id={}, proj_id={}, dataset_name='{}', datatable_name='{}', origin_filepath='{}', origin_filetype='{}';".format(
            dataset_id, proj_id, dataset_name, datatable_name, origin_filepath, origin_filetype)
        self.res.adu_sql(sql)

    # project_id
    def select_dataset_id(self, proj_id):
        # proj_id, user_id, proj_name
        sql = "select dataset_id from `dataset` where proj_id={}".format(proj_id)
        project_id = self.res.select_sql(sql)
        return project_id

    def close(self):
        self.res.close()


if __name__ == '__main__':
    ret = insert_project_infor()
    res = ret.select_project_id(12, 'abcde')
    print(res)
    ret.close()