#!/usr/bin/env python
# -*- coding:utf-8 -*-

from models.base import base_model


def download_data(libname, tablename):
    sql = "select * from `{}`".format(tablename)
    res = base_model(libname).connect()
    query_result = res.select_sql(sql)
    res.close()
    return query_result


