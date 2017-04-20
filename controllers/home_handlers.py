#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

class BaseController(tornado.web.RequestHandler):
    def render(self, tpl, **render_data):
        if not tpl.endswith('html'):
            tpl = "{}.html".format(tpl)
        super(BaseController, self).render(tpl, **render_data)
class My404(BaseController):
    def get(self):
        self.render('404')

def write_error(self, stat, **kw):
    # self.write('访问url不存在!')
    self.render('404.html')