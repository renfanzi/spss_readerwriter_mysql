#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

data = dict(user_id=12, project_name=14, dataset_id=40)
requests.post(url = "http://127.0.0.1:8001/download", data=data)