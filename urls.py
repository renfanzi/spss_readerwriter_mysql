#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers.updownload_handler import Upload, Writer_Spss_Mysql

urls = [
    (r'/upload', Upload),
    (r'/writer_spss_mysql', Writer_Spss_Mysql),
]