#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers.upload_handler import MainHandler

urls = [
    (r'/index', MainHandler),
]