

## 功能
```
1. 将文件上传（spss类型文件）并获取数据写入数据库
2. 获取内容生成spss文件
```

## 过程
1. 读取文件，得到列名和类型
2. 创建表
3. 存入数据--注意对时间的处理和指标签和说明 确定对mysql的处理
4. 读取数据返回web  暂缓
5. 日志
6. 异步处理


## 注意事项:
    1. Python版本2.7.12, 注意对汉字对unicode的处理
    2. 在存入库的时候将unicode的字符串进行了json(类型为VARCHAR)
    3. 时间模块存库的时候是字符串,不是json
    4. 字典, key为int, value为字符串时候,进行json, key会变成float, 反解的时候不能变成int, 重点是valueLables
    5. 对汉字的处理, savwrite的时候: ioutf-8, 看用途吧
    6. 对时间的处理 暂时只支持这两种b = "2016-11-15"  c = u'2016-09-21 13:37:34'


## 删除所有.pyc文件的命令
```find 绝对路径  -type f -name  "*.pyc"  | xargs -i -t rm -f {}```

## git上传命令
```
git add .
git commit -m ""
git push origin master
```

## 基础核心用法
```
import datetime

savFileName = '/opt/someFile.sav'
varNames = [u'ID', u'StartTime', u'EndTime', u'VerNo', u'Q1', u'Q2', u'Q4']
varTypes = {u'Q1': 0, u'Q2': 400, u'Q4': 400, u'StartTime': 0, u'VerNo': 0, u'EndTime': 0, u'ID': 20}
varLabels = {u'Q1': u'\u5546\u8d85\u914d\u9001\u6536\u8d39\u6807\u51c6\u6b63\u786e\u7684\u662f', u'Q2': u'\u5546\u8d85\u4e0a\u7ebf\u6807\u51c6', u'Q4': u'\u672c\u6b21\u57f9\u8bad\u6536\u83b7\u548c\u610f\u89c1', u'StartTime': u'\u5f00\u59cb\u65f6\u95f4', u'VerNo': u'\u7248\u672c', u'EndTime': u'\u7ed3\u675f\u65f6\u95f4', u'ID': u'\u7528\u6237'}
valueLabels = {'Q1': {1.0: u'\u4e13\u9001\u6536\u8d39', 2.0: u'\u5feb\u9001\u6536\u8d39'}, u'Q2': {}, u'Q4': {}, 'StartTime': {}, 'VerNo': {}, 'EndTime': {}, 'ID': {}}
formats = {u'Q1': u'F5.0', u'VerNo': u'F5.0', u'EndTime': 'DATETIME40', u'StartTime': 'DATETIME40'}
data = [[u'lKWmel1491380676', 13710788676.0, 13710788696.0, 1L, 1, u'\u725b\u820c', u'\u6e56\u516c\u56ed\u80e1\u5a77']]
# 时间模块这样是错误的data = [[u'lKWmel1491380676', datetime.datetime(2016, 9, 21, 13, 42, 8), datetime.datetime(2016, 9, 21, 13, 42, 8), 1L, 1, u'\u725b\u820c', u'\u6e56\u516c\u56ed\u80e1\u5a77']]
#
# with SavWriter(savFileName, varNames, varTypes, varLabels=varLabels, columnWidths={}, ioUtf8=True) as writer:
#     writer.writerows(data)
with SavWriter(savFileName=savFileName, varNames=varNames, varTypes=varTypes,
               varLabels=varLabels, valueLabels=valueLabels, ioUtf8=True, formats=formats,
               columnWidths={}) as writer:

    writer.writerows(data)
```

## 错误信息的原因
通常一下错误的原因是因为头部数据信息和data数据不对称,数据列不对等造成的
```
Traceback (most recent call last):
  File "/opt/code/test_code/SpssMysql_and_SyntheticSpss/controllers/download_handler.py", line 92, in <module>
    varLabels=varLabels, ioUtf8=True) as writer:
  File "/usr/local/lib/python2.7/dist-packages/savReaderWriter/savWriter.py", line 220, in __init__
    self.varNamesTypes = self.varNames, self.varTypes
  File "/usr/local/lib/python2.7/dist-packages/savReaderWriter/header.py", line 200, in varNamesTypes
    checkErrsWarns(msg, retcode)
  File "/usr/local/lib/python2.7/dist-packages/savReaderWriter/error.py", line 120, in checkErrsWarns
    raise SPSSIOError(msg, retcode)
savReaderWriter.error.SPSSIOError: Problem setting variable name 'ID' [SPSS_DUP_VAR]
```