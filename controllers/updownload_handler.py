#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado
from tornado.web import RequestHandler
import json
import os
import random
import datetime, time
import requests
from common.base import result
# from core.spss_upload import main
from common.base import Config
from core.spss_upload import upload_spss
from common.base import my_log
from core.spss_download import spss_main
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

""""""
class Upload(RequestHandler):
    executor = ThreadPoolExecutor(2)


    def get(self):
        self.render('upload.html')

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        file_metas = self.request.files["file"]
        user_id = self.get_arguments("user_id")[0]
        project_name = self.get_arguments("project_name")[0]
        if not (user_id and project_name):
            self.write(json.dumps(result(4000, value=None), ensure_ascii=False))
            return

        for meta in file_metas:
            file_name = meta['filename']
            if file_name.split(".")[-1] != "sav":
                self.write(json.dumps(result(4000, value=None), ensure_ascii=False))
                return
            #这块对路径的修改和文件目录的创建
            file_path = Config().get_content('filepath')['upload_path']

            # 判断file_path 下面有没有user_id 文件目录, 没有创建一个
            user_file_path = os.path.join(file_path, str(user_id))
            time_now = datetime.datetime.now().strftime("%Y-%m-%d")
            user_subfilepath = os.path.join(user_file_path, time_now)

            if not os.path.exists(user_file_path):
                os.makedirs(user_file_path)

            if not os.path.exists(user_subfilepath):
                os.makedirs(user_subfilepath)

            if os.path.exists(os.path.join(user_subfilepath, file_name)):
                os.renames(os.path.join(user_subfilepath, file_name), os.path.join(user_subfilepath, file_name+".bak"))

            # file_path = os.path.join("file", file_name)
            # write input file --file
            with open(os.path.join(user_subfilepath, file_name), 'wb') as up:
                up.write(meta['body'])
        a = time.time()
        res = yield self.sleep(user_subfilepath, file_name, user_id, project_name)
        b = time.time() - a
        print(b)
        self.write(json.dumps(result(2000, value={}), ensure_ascii=False))
        self.finish()

    @run_on_executor
    def sleep(self, user_subfilepath, file_name, user_id, project_name):
        ret = requests.post('http://127.0.0.1:8001/writer_spss_mysql',
                            data={"file_path": user_subfilepath,
                                  "file_name": file_name,
                                  "user_id": user_id,
                                  "project_name": project_name})
        return ret.text


class Writer_Spss_Mysql(RequestHandler):
    executor = ThreadPoolExecutor(2)

    def get(self):
        self.write(json.dumps("孙子,快叫爷爷", ensure_ascii=False))

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # user_id, project 都要拿到
        file_path = self.get_arguments("file_path")[0]
        file_name = self.get_arguments("file_name")[0]
        user_id = self.get_arguments("user_id")[0]
        project_name = self.get_arguments("project_name")[0]

        # ret = main(file_path, file_name, user_id, project_name)
        ret = upload_spss().main(file_path, file_name, user_id, project_name)
        self.write(json.dumps(result(2000, value={}), ensure_ascii=False))
        self.finish()


class Download(RequestHandler):
    executor = ThreadPoolExecutor(2)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 缺失一次判断
        user_id = self.get_arguments("user_id")[0]
        project_name = self.get_arguments("project_name")[0]
        dataset_id = self.get_arguments("dataset_id")[0]

        res = yield self.sleep(user_id, project_name, dataset_id)

        self.write(json.dumps(result(2000, value={"filepath": res}), ensure_ascii=False))
        self.finish()

    @run_on_executor
    def sleep(self, user_id, project_name, dataset_id):
        ret = requests.post('http://127.0.0.1:8001/generate_spssfile',
                            data={"user_id": user_id,
                                  "project_name": project_name,
                                  "dataset_id": dataset_id})
        return ret.text


class Generate_SpssFile(RequestHandler):
    executor = ThreadPoolExecutor(2)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        user_id = self.get_arguments("user_id")[0]
        project_name = self.get_arguments("project_name")[0]
        dataset_id = self.get_arguments("dataset_id")[0]
        filepathname = spss_main(user_id, project_name, dataset_id).genreate_spss()
        self.write(json.dumps(result(2000, value={"filepath": filepathname}), ensure_ascii=False))
        self.finish()

if __name__ == '__main__':
    file_path = Config().get_content('filepath')['upload_path']
    print(file_path)