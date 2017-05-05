#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 合成spss文件
import json
import os
import time, datetime
import pickle
from savReaderWriter import SavWriter
from models.download_file import select_tableinfor, select_data, select_infor
from common.base import my_datetime, Config

# varNames = []
# varTypes = {}
# varLabels = {}
# valueLabels = {}
# formats = {}
# my_columns_types = []
#
# data = []


# query_information = download_data('information', '1111.sav')
# query_data = download_data('data', '1111.sav')


# for i in query_information:
#     name = i["name"]
#     my_columns_types.append(i["type"])
#     varNames.append(name)
#
#     if i["formats"].startswith("F") or i["formats"].startswith("D"):
#         varTypes[name] = 0
#     elif i["formats"].startswith("A"):
#         varTypes[name] = int(i["formats"].split("A")[1])
#     else:
#         varTypes[name] = 0
#
#     # varLabels[name] = json.loads(i["varlabels"])
#     varLabels[name] = i["varlabels"]
#     if i["valuelabels"]:
#         res2 = i["valuelabels"]
#         if res2 == "0":
#             valueLabels[name] = {}
#         else:
#             res3 = json.loads(res2)
#             # 再次进行判断,json以后浮点变字符串
#             if isinstance(res3, dict):
#                 res4 = {}
#                 for k, v in res3.items():
#                     j = float(k)
#                     res4[j] = v
#
#             valueLabels[name] = res4
#
#     else:
#         valueLabels[name] = {}
#
#     formats[name] = i["formats"]


# mdt = my_datetime()
# savFileName = '/opt/someFile.sav'
# with SavWriter(savFileName=savFileName, varNames=varNames, varTypes=varTypes,
#                formats=formats, varLabels=varLabels, valueLabels=valueLabels,
#                ioUtf8=True, columnWidths={}) as writer:
#     for row_data in query_data:
#         sub_li = []
#         for i in range(len(my_columns_types)):
#
#             sub_data = row_data[varNames[i]]
#
#             if my_columns_types[i] == "VARCHAR":
#                 sub_li.append(sub_data)
#             elif my_columns_types[i] == "DATETIME":
#                 aaa = mdt.become_str(sub_data)
#                 sub_li.append(writer.spssDateTime(bytes(aaa, 'utf-8'), '%Y-%m-%d %H:%M:%S'))
#             elif my_columns_types[i] == "DATE":
#                 sub_li.append(writer.spssDateTime('%s' % sub_data, '%Y-%m-%d'))
#             else:
#                 sub_li.append(sub_data)
#         data.append(sub_li)
#
#     writer.writerows(data)

class spss_main():
    def __init__(self, user_id, proj_id, dataset_id):
        self.user_id = user_id
        self.proj_id = proj_id
        self.dataset_id = dataset_id
        self.varNames = []
        self.varTypes = {}
        self.varLabels = {}
        self.valueLabels = {}
        self.formats = {}
        self.my_columns_types = []

        self.data = []
        self.query_information = None
        self.query_data = []
        self.table_infor = None
        self.my_data = None

    def get_data(self):
        self.table_infor = select_tableinfor(self.proj_id, self.dataset_id)
        for i in self.table_infor:
            self.query_data.append(select_data(i["datatable_name"]))
        # self.query_data = [[[...],[...]..], [....].....]
        self.my_data = self.query_data[0]
        for i in range(1, len(self.query_data)):
            for j in range(len(self.my_data)):
                self.my_data[j] += self.query_data[i][j]

        self.query_information = select_infor(self.proj_id, self.dataset_id)

        return self.query_information, self.my_data

    def adjust_data(self):
        query_information, query_data = self.get_data()
        for i in query_information:
            name = i["name"]
            self.my_columns_types.append(i["type"])
            self.varNames.append(name)

            if i["formats"].startswith("F") or i["formats"].startswith("D"):
                self.varTypes[name] = 0
            elif i["formats"].startswith("A"):
                self.varTypes[name] = int(i["formats"].split("A")[1])
            else:
                self.varTypes[name] = 0
            self.varLabels[name] = i["varlabels"]
            if i["valuelabels"]:
                res2 = i["valuelabels"]
                if res2 == "0":
                    self.valueLabels[name] = {}
                else:
                    res3 = json.loads(res2)
                    # 再次进行判断,json以后浮点变字符串
                    if isinstance(res3, dict):
                        res4 = {}
                        for k, v in res3.items():
                            j = float(k)
                            res4[j] = v

                    self.valueLabels[name] = res4

            else:
                self.valueLabels[name] = {}

            self.formats[name] = i["formats"]

    def genreate_spss(self):
        self.adjust_data()
        mdt = my_datetime()
        nowtime = datetime.datetime.now().strftime("%Y%m%d")
        new_time1 = "%.6f" % float(time.time())
        new_time3 = new_time1.split(".")[0] + new_time1.split(".")[1]
        filename = "u" + str(self.user_id) + "_" + str(nowtime) + "_" + str(new_time3)
        filepath = Config().get_content("filepath")["download_path"]
        if filepath:
            user_file_path = os.path.join(filepath, str(self.user_id))
            time_now = datetime.datetime.now().strftime("%Y-%m-%d")
            user_subfilepath = os.path.join(user_file_path, time_now)

            if not os.path.exists(user_file_path):
                os.makedirs(user_file_path)

            if not os.path.exists(user_subfilepath):
                os.makedirs(user_subfilepath)

        else:

            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "download")
            user_file_path = os.path.join(filepath, str(self.user_id))
            time_now = datetime.datetime.now().strftime("%Y-%m-%d")
            user_subfilepath = os.path.join(user_file_path, time_now)

            if not os.path.exists(user_file_path):
                os.makedirs(user_file_path)

            if not os.path.exists(user_subfilepath):
                os.makedirs(user_subfilepath)

        savFileName= os.path.join(user_subfilepath, filename + ".sav")
        print(self.varLabels)
        with SavWriter(savFileName=savFileName, varNames=self.varNames, varTypes=self.varTypes,
                       formats=self.formats, varLabels=self.varLabels, valueLabels=self.valueLabels,
                       ioUtf8=True, columnWidths={}) as writer:
            for row_data in self.my_data:
                sub_li = []
                for i in range(len(self.my_columns_types)):

                    sub_data = row_data[self.varNames[i]]

                    if self.my_columns_types[i] == "VARCHAR":
                        sub_li.append(sub_data)
                    elif self.my_columns_types[i] == "DATETIME":
                        aaa = mdt.become_str(sub_data)
                        sub_li.append(writer.spssDateTime(bytes(aaa, 'utf-8'), '%Y-%m-%d %H:%M:%S'))
                    elif self.my_columns_types[i] == "DATE":
                        sub_li.append(writer.spssDateTime('%s' % sub_data, '%Y-%m-%d'))
                    else:
                        sub_li.append(sub_data)
                self.data.append(sub_li)

            writer.writerows(self.data)

        return savFileName

if __name__ == '__main__':
    filepathname = spss_main(12, 14, 23).genreate_spss()
    print(filepathname)