# !/usr/bin/env python
# -*- coding:utf-8 -*-

class BaseDao():
    __result = {}
    __parameter = {}

    def __init__(self, parameter=None):
        self.__parameter = parameter

