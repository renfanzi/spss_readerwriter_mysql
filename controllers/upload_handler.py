#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado
import json
import os
from common.base import result
from core.spss_upload import main

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self, *args, **kwargs):
        file_metas = self.request.files["inputfile"]
        # print(file_metas)
        for meta in file_metas:
            file_name = meta['filename']

            if file_name.split(".")[-1] != "sav":
                self.write(json.dumps(result(4000, value=None), ensure_ascii=False))
                return

            file_path = os.path.join("file", file_name)
            # write input file --file
            with open(file_path, 'wb') as up:
                up.write(meta['body'])

        ret = main(file_name)
        if ret != 2000:
            self.write(json.dumps(result(ret, value=None), ensure_ascii=False))
            return

        self.write(json.dumps(result(2000, value={}), ensure_ascii=False))