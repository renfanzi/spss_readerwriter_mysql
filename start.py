#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import os
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from controllers.home_handlers import My404, write_error
from common.util.include_url_model import url_wrapper, include


define("port", default=8000, type=int)
_ROOT_PATH = os.path.dirname(__file__)
ROOT_JOIN = lambda sub_dir: os.path.join(_ROOT_PATH, sub_dir)


router = url_wrapper([
    (r'', include('urls')),
])


settings = dict(
    template_path=ROOT_JOIN('views'),
    static_path=ROOT_JOIN('static'),
    # cookie_secret=Env.COOKIE_SEC,
    default_handler_class=None
)


tornado.web.RequestHandler.write_error = write_error
application = tornado.web.Application(router, **settings)


if __name__ == "__main__":
    server = HTTPServer(application)
    server.bind(options.port)
    server.start(1)  # Forks multiple sub-process
    tornado.ioloop.IOLoop.current().start()
