#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Do:

    def ok(self, idata={}):
        data = {}
        data["bool"] = 1
        data["data"] = idata
        return data

    def error(self):
        data = {}
        data["bool"] = 0
        data["data"] = {}
        return data