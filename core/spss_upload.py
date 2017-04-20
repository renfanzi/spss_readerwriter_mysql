#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
import pickle
import savReaderWriter
from common.base import MongoDb, Config
import time, os
from collections import OrderedDict
import pymysql
from common.log.loger import my_log
from common.base import my_datetime
from models.create_tables import create_data_table, writer_data_table
from models.create_tables import create_information_tables, writer_information_tables

vartypes = []  # ['A20', 'F8.2', 'F8', 'DATETIME20'] spss类型
width = []  # ['20', '8.2', '8', '20'] 宽度
valuetypes = []  # 数据类型
float_width = []


# 获取文件详细信息
def read_sav(filepath):
    with savReaderWriter.SavReader(filepath, ioUtf8=True) as read:
        ret = read.getSavFileInfo()
        """
        # getsavfileinfo infomation :
        # (self.numVars, self.nCases, self.varNames, self.varTypes,self.formats, self.varLabels, self.valueLabels)
        """
        return read.formats, read.varNames, read.varLabels, read.valueLabels


# 写入数据到数据库
def writer_data(filepath, filename, valuetypes):
    res = writer_data_table()
    with savReaderWriter.SavReader(filepath, ioUtf8=True) as read:
        # 如果不用ioutf8， 汉字十六进制\被转义，更麻烦
        for i in read:
            for j in range(len(valuetypes)):
                # 数据库不认unicode所以要转换下
                # 将varchar进行json存如数据库
                if valuetypes[j] == "DATETIME":
                    i[j] = read.spss2strDate(i[j], '%Y-%m-%d %H:%M:%S', None)
                elif valuetypes[j] == "DATE":
                    i[j] = read.spss2strDate(i[j], '%Y-%m-%d', None)
                elif valuetypes[j] == "VARCHAR":
                    i[j] = i[j]
            res.insert_sql(filename, i)
    res.close()

# 获取spss需要的一些数据
def get_spss_data(formats, varnames):
    for i in varnames:
        vartypes.append(formats[i])
        if formats[i].startswith("F"):
            ret = formats[i].split("F")[1]
            width.append(ret)
            ret1 = ret.split(".")
            if ret1[1:]:
                valuetypes.append("FLOAT")
            else:
                valuetypes.append("INT")

        elif formats[i].startswith("A"):
            ret = formats[i].split("A")[1]
            width.append(ret)
            valuetypes.append("VARCHAR")

        elif formats[i].startswith("DATE"):
            if formats[i].split("DATE")[1].startswith("TIME"):
                ret = formats[i].split("DATETIME")[1]
                width.append(ret)
                valuetypes.append("DATETIME")
            else:
                ret = formats[i].split("DATE")[1]
                width.append(ret)
                valuetypes.append("DATE")
    return vartypes, width, valuetypes


# 进行切割,判断是不是有浮点位的,如果没有填充0,生成文件要用
def float_data(width):
    for i in width:
        if i.split(".")[1:]:
            float_width.append(i[1])
        else:
            float_width.append(0)
    return float_width


# 判断是字典还是字符串, 进行decode
def valuelables_decode(unicode_dict):
    if isinstance(unicode_dict, dict):
        for i in unicode_dict:
            unicode_dict[i] = unicode_dict[i].decode('utf-8')
        return unicode_dict
    elif isinstance(unicode_dict, str):
        return unicode_dict.decode('utf-8')


# 插入信息表的数据
def insert_sub_table(filename, varnames, valuetypes, width, float_width, varLabels, valueLabels, vartypes):
    res = writer_information_tables()

    for i in range(len(varnames)):
        data = []
        data.append(varnames[i])
        data.append(valuetypes[i])
        data.append(width[i])
        data.append(float_width[i])
        # data.append(varLabels[varnames[i]].replace('\u3000', ' '))  # 注意这里: 存之前: Ｆ1.0　请根据你的实际情况，  存之后:Ｆ4.0u3000请根据你的实际情况，在下列描述中，选择符合你的程度，并选择
        data.append(varLabels[varnames[i]].replace('\u3000', ' '))
        if varnames[i] in valueLabels:
            json_unicode_dict = json.dumps(valueLabels[varnames[i]], ensure_ascii=False)
            data.append(json_unicode_dict)
        else:
            data.append(0)
        data.append(vartypes[i])
        data.append("")
        data.append("")
        # sql = res.insert_sql(filename, data)
        res.insert_sql(filename, data)
    res.close()


def main(filename):

    """
    # print(formats):{'Q8': 'A400', 'Q3R6': 'F5', 'Q5R3': 'F5', }
    # print(varnames)['ID', 'StartTime', 'EndTime', 'VerNo', 'Q1R3',]
    # print(varLabels){'Q8': 'Q2. 学号', 'Q3R6': 'Ｆ2.2\u3000请根据你的实际情况，
    # print(valueLabels){'Q3R6': {1.0: '非常不符合', 2.0: '比较不符合',
    # print("vartypes", my_vartypes) ['A20', 'DATETIME40', 'DATETIME40',
    # print(width) ['20', '40', '40', '5', '5', '5', '5',
    # print(my_valuetypes) ['VARCHAR', 'DATETIME', 'DATETIME', 'INT',
    # print(float_width)[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    """

    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file", filename)
    # 得到文件信息
    formats, varnames, varLabels, valueLabels = read_sav(filepath)
    #不允许超过1024列MySQL
    if len(varnames) > 1024:
        return 4001

    my_vartypes, my_width, my_valuetypes = get_spss_data(formats, varnames)
    float_width = float_data(width)
    for i in range(len(my_vartypes)):
        if my_vartypes[i].startswith("F"):
            if my_vartypes[i].split(".")[1:]:
                pass
            else:
                my_vartypes[i] = my_vartypes[i] + ".0"

    # 创建表
    create_data_table(my_vartypes, my_width, my_valuetypes, formats, varnames, filename)
    writer_data(filepath, filename, valuetypes)


    create_information_tables(filename)
    # 写入数据
    insert_sub_table(filename, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels, my_vartypes)

    # if ret==2000 and ret1 == 2000:
    #     return ret
    # else:
    #     return 5000


if __name__ == '__main__':
    filename = "1111.sav"
    main(filename)
