#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers.updownload_handler import Upload, Writer_Spss_Mysql, Generate_SpssFile, Download

urls = [
    (r'/upload', Upload),
    (r'/writer_spss_mysql', Writer_Spss_Mysql),
    (r'/download', Download),
    (r'/generate_spssfile', Generate_SpssFile),
]