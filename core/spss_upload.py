#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import savReaderWriter
import os
from common.base import my_log
from models.create_tables import create_data_table, writer_data_table
from models.create_tables import create_information_tables, writer_information_tables
from models.create_tables import insert_project_infor

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


# 写入数据到数据库
def writer_data(filepath, tablename, valuetypes):
    res = writer_data_table()
    with savReaderWriter.SavReader(os.path.join(filepath, tablename), ioUtf8=True) as read:
        # 如果不用ioutf8， 汉字十六进制\被转义，更麻烦
        try:
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
                res.insert_sql(tablename, i)
        except Exception as e:
            my_log.error(e)
        finally:
            my_log.info("data write database success !!!")
    res.close()



def writer_moredata(filepath, tablename, valuetypes, start, end):
    res = writer_data_table()
    with savReaderWriter.SavReader(os.path.join(filepath, tablename), ioUtf8=True) as read:
        # 如果不用ioutf8， 汉字十六进制\被转义，更麻烦
        try:
            for i in read:
                i = i[start:end]
                for j in range(len(valuetypes)):
                    # 数据库不认unicode所以要转换下
                    # 将varchar进行json存如数据库
                    if valuetypes[j] == "DATETIME":
                        i[j] = read.spss2strDate(i[j], '%Y-%m-%d %H:%M:%S', None)
                    elif valuetypes[j] == "DATE":
                        i[j] = read.spss2strDate(i[j], '%Y-%m-%d', None)
                    elif valuetypes[j] == "VARCHAR":
                        i[j] = i[j]
                res.insert_sql(tablename, i)
        except Exception as e:
            my_log.error(e)
        finally:
            my_log.info("data write database success !!!")
    res.close()

# 插入信息表的数据
def insert_sub_table(filename, varnames, valuetypes, width, float_width, varLabels, valueLabels, vartypes, project_id, dataset_id):
    res = writer_information_tables()

    for i in range(len(varnames)):
        data = []
        data.append(project_id)
        data.append(dataset_id)
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
        res.insert_sql("data_information", data)
    res.close()


def main(filepath, filename, user_id, project_name):

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

    # filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file", filename)
    FilePathName = os.path.join(filepath, filename)
    print("filepath: ",FilePathName)
    # 得到文件信息
    formats, varnames, varLabels, valueLabels = read_sav(FilePathName)
    my_vartypes, my_width, my_valuetypes = get_spss_data(formats, varnames)
    float_width = float_data(width)
    for i in range(len(my_vartypes)):
        if my_vartypes[i].startswith("F"):
            if my_vartypes[i].split(".")[1:]:
                pass
            else:
                my_vartypes[i] = my_vartypes[i] + ".0"

    insert_project = insert_project_infor()
    # project表
    project_id = insert_project.select_project_id(user_id, project_name)[-1]["proj_id"]
    if not project_id:
        project_id = insert_project.insert_project(user_id, project_name)

    #先查dataset的id,然后在插入
    # dataset_id, proj_id, dataset_name, datatable_name, origin_filepath, origin_filetype
    print(project_id)
    dataset_id_group = insert_project.select_dataset_id(project_id)
    print('ddddd',dataset_id_group)
    if not dataset_id_group:
        dataset_id = 1
    else:
        print(dataset_id_group)
        dataset_id = dataset_id_group[-1]["dataset_id"] + 1

    print(dataset_id)


    # 创建表
    #不允许超过1024列MySQL, 超过了分表
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d")
    if len(varnames) < 1024:
        table_name = user_id + "_" + nowtime + "_" + filename

        create_data_table(my_vartypes, my_width, my_valuetypes, formats, varnames, filename, table_name)
        writer_data(filepath, filename, my_valuetypes)
        print("aaa")
        insert_project.insert_dataset(dataset_id, project_id, filename,filename, filepath, ".sav")
    else:
        integer, remainder = divmod(len(varnames), 800)
        if remainder:
            integer += 1
        for num in range(1, integer+1):
            table_subname = filename + "_" + num

            table_subname = user_id + "_" + nowtime + "_" + table_subname
            insert_project.insert_dataset(dataset_id, project_id, filename, filename, filepath, ".sav")
            start = i*800-800
            end = i*800
            create_data_table(my_vartypes[start:end], my_width[start:end], my_valuetypes[start:end],
                              formats[start:end], varnames[start:end], table_subname, user_id)
            writer_moredata(filepath, filename, my_valuetypes[start:end], start, end)
    insert_project.close()
    # 信息表值创建一个
    # create_information_tables(filename)
    # 写入数据
    insert_sub_table(filename, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels, my_vartypes, project_id, dataset_id)

    # if ret==2000 and ret1 == 2000:
    #     return ret
    # else:
    #     return 5000


if __name__ == '__main__':
    filename = "1111.sav"
    main(filename)
