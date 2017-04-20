#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 合成spss文件
import json
import pickle
from savReaderWriter import SavWriter
from models.download_file import download_data
from common.base import my_datetime

varNames = []
varTypes = {}
varLabels = {}
valueLabels = {}
formats = {}
my_columns_types = []

data = []


def spss_download():
    pass

query_information = download_data('information', '1111.sav')
query_data = download_data('data', '1111.sav')


for i in query_information:
    name = i["name"]
    my_columns_types.append(i["type"])
    varNames.append(name)

    if i["formats"].startswith("F") or i["formats"].startswith("D"):
        varTypes[name] = 0
    elif i["formats"].startswith("A"):
        varTypes[name] = int(i["formats"].split("A")[1])
    else:
        varTypes[name] = 0

    # varLabels[name] = json.loads(i["varlabels"])
    varLabels[name] = i["varlabels"]
    if i["valuelabels"]:
        res2 = i["valuelabels"]
        if res2 == "0":
            valueLabels[name] = {}
        else:
            res3 = json.loads(res2)
            # 再次进行判断,json以后浮点变字符串
            if isinstance(res3, dict):
                res4 = {}
                for k, v in res3.items():
                    j = float(k)
                    res4[j] = v

            valueLabels[name] = res4

    else:
        valueLabels[name] = {}

    formats[name] = i["formats"]


mdt = my_datetime()
savFileName = '/opt/someFile.sav'
with SavWriter(savFileName=savFileName, varNames=varNames, varTypes=varTypes,
               formats=formats, varLabels=varLabels, valueLabels=valueLabels,
               ioUtf8=True, columnWidths={}) as writer:
    for row_data in query_data:
        sub_li = []
        for i in range(len(my_columns_types)):

            sub_data = row_data[varNames[i]]

            if my_columns_types[i] == "VARCHAR":
                sub_li.append(sub_data)
            elif my_columns_types[i] == "DATETIME":
                aaa = mdt.become_str(sub_data)
                sub_li.append(writer.spssDateTime(bytes(aaa, 'utf-8'), '%Y-%m-%d %H:%M:%S'))
            elif my_columns_types[i] == "DATE":
                sub_li.append(writer.spssDateTime('%s' % sub_data, '%Y-%m-%d'))
            else:
                sub_li.append(sub_data)
        data.append(sub_li)

    writer.writerows(data)

