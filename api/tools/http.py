# !/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, Response
import json
import demjson
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def ok(msg='ok', idata={}):
    data = {}
    data["code"] = 200
    data["msg"] = msg
    data["data"] = idata
    jsonData = json.dumps(data, cls=MyEncoder, ensure_ascii=False, indent=4)
    return Response(jsonData, mimetype='application/json')


def loadOk():
    data = {}
    data["success"] = True
    data["message"] = "上传成功"
    jsonData = json.dumps(data, cls=MyEncoder, ensure_ascii=False, indent=4)
    return Response(jsonData, mimetype='application/json')


def loadErr(msg=None):
    data = {}
    data["success"] = False
    if msg == None:
        data["message"] = "上传失败"
    else:
        data["message"] = msg
    jsonData = json.dumps(data, cls=MyEncoder, ensure_ascii=False, indent=4)
    return Response(jsonData, mimetype='application/json')


def error(msg='error', code=204):
    data = {}
    data["code"] = code
    data["msg"] = msg
    data["data"] = []
    jsonData = json.dumps(data, cls=MyEncoder, ensure_ascii=False, indent=4)
    return Response(jsonData, mimetype='application/json')


def req():
    data = demjson.decode(request.data.decode(encoding='utf-8'))
    return data


def jsonData(idata={}):
    jsonData = json.dumps(idata, cls=MyEncoder, ensure_ascii=False, indent=4)
    return jsonData
