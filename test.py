#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json, pickle
import datetime, time
#
# def valuelables_decode(unicode_dict):
#     if isinstance(unicode_dict, dict):
#         for i in unicode_dict:
#             unicode_dict[int(i)] = unicode_dict[i].decode('utf-8')
#         return unicode_dict
#     elif isinstance(unicode_dict, str):
#         return unicode_dict.decode('utf-8')
#
#
# if __name__ == '__main__':
#     d = {1.0: '\xe7\x94\xb7', 2.0: '\xe5\xa5\xb3'}
#     res = valuelables_decode(d)
#     print res
#     res1 = pickle.dumps(d)
#     print res1
#     res2 = pickle.loads(res1)
#     print 'aaa',res2
#

"""

class my_datetime():
    def __init__(self):
        # 缺少对utc时间的判断a
        pass

    def become_timestamp(self, dtdt):
        # 将时间类型转换成时间戳
        if isinstance(dtdt, datetime.datetime):
            timestamp = time.mktime(dtdt.timetuple())
            return timestamp

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d  %H:%M:%S")
                timestamp = time.mktime(a_datetime.timetuple())
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                timestamp = time.mktime(a_datetime.timetuple())
            return timestamp

        elif isinstance(dtdt, float):
            return dtdt

        elif isinstance(dtdt, unicode):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
                timestamp = time.mktime(a_datetime.timetuple())
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                timestamp = time.mktime(a_datetime.timetuple())
            return timestamp

    def become_datetime(self, dtdt):
        # 将时间类型转换成datetime类型
        if isinstance(dtdt, datetime.datetime):
            return dtdt

        elif isinstance(dtdt, str):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            return a_datetime

        elif isinstance(dtdt, float):
            # 把时间戳转换成datetime类型
            a_datetime = datetime.datetime.fromtimestamp(dtdt)
            return a_datetime

        elif isinstance(dtdt, unicode):
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
            return a_datetime

    def become_str(self, dtdt):
        # 把时间类型转换成字符串
        if isinstance(dtdt, datetime.datetime):
            a_datetime = dtdt.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

        elif isinstance(dtdt, str):
            return dtdt

        elif isinstance(dtdt, float):
            a_datetime_local = datetime.datetime.fromtimestamp(dtdt)
            a_datetime = a_datetime_local.strftime("%Y-%m-%d %H:%M:%S")
            return a_datetime

        elif isinstance(dtdt, unicode):
            # 区别：一个是strp， 一个是strf
            if dtdt.split(" ")[1:]:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d %H:%M:%S")
                a_datetime = a_datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                a_datetime = datetime.datetime.strptime(dtdt, "%Y-%m-%d")
                a_datetime = a_datetime.strftime("%Y-%m-%d")
            # return a_datetime

if __name__ == '__main__':
    a = datetime.datetime(2016, 9, 21, 13, 42, 8)
    b = "2016-11-15"
    c = u'2016-09-21'
    print type(c)
    d = 1474436826.0
    e = 13710788676.0
    ret = my_datetime()
    res = ret.become_str(c)
    print res
    print type(res)

"""



