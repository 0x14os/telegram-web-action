# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.conf import db_host, db_port, db_user, db_pass, db_use_data,debug

dblink = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (db_user, db_pass, db_host, db_port, db_use_data)

# print(dblink)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tg_'
app.config['SQLALCHEMY_DATABASE_URI'] = dblink
# 在app设置里开启自动提交 & 每次请求结束后都会自动提交数据库中的变动.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
# 关闭数据追踪，避免内存资源浪费
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 如果设置为Ture,SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。
app.config['SQLALCHEMY_ECHO'] = debug
# 可以用于显式地禁用或启用查询记录。查询记录 在调试或测试模式自动启用。更多信息见
# app.config['SQLALCHEMY_RECORD_QUERIES'] = False

# app.config['SQLALCHEMY_AUTO_FLUSH'] = True

db = SQLAlchemy(app,session_options={"autoflush": False})

# class AlchemyEncoder(json.JSONEncoder):
#     """
#     SqlAlchemy对象转换为json格式
#     """
#
#     def default(self, obj):
#
#         if isinstance(obj.__class__, DeclarativeMeta):
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     if type(data) is datetime.datetime:
#                         data = data.strftime("%Y-%m-%d %H:%M:%S")
#                     else:
#                         json.dumps(data)
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             return fields
#         return json.JSONEncoder.default(self, obj)
