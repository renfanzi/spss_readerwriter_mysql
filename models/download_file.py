#!/usr/bin/env python
# -*- coding:utf-8 -*-

from models.base import base_model

# 需要三个数据
# 2. information
# 3. data
# 1. 数据表等信息

def select_tableinfor(proj_id, dataset_id, libname="user_information"):
    sql = """select datatable_name from dataset where proj_id={} and dataset_id={}""".format(proj_id, dataset_id)
    res = base_model(libname).connect()
    query_result = res.select_sql(sql)
    res.close()
    return query_result


def select_data(tablename, libname="data"):
    sql = """select * from {}""".format(tablename)
    res = base_model(libname).connect()
    query_result = res.select_sql(sql)
    res.close()
    return query_result


def select_infor(proj_id, dataset_id, libname="user_information"):
    sql = """select `name`, `type`, `width`, `float_width`, `varlabels`, `valuelabels`, `formats` from `data_information` where project_id={} and dataset_id={}""".format(proj_id, dataset_id)
    res = base_model(libname).connect()
    query_result = res.select_sql(sql)
    res.close()
    return query_result


if __name__ == '__main__':
    ret = select_infor(14, 23)
    print(ret)
