#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

from config.conf import redis_ip, redis_port, redis_passwd, redis_pool, redis_use_db_user


class RedisCon(object):
    __db = None

    def __init__(self, name=None, namespace='queue', **redis_kwargs):
        if redis_pool:
            pool = redis.ConnectionPool(host=redis_ip, port=redis_port, password=redis_passwd, charset="utf-8",
                                        db=redis_use_db_user,
                                        decode_responses=True)
            self.__db = redis.Redis(connection_pool=pool)
        else:
            if name == "aps":
                self.__db = redis.Redis(host=redis_ip, port=redis_port, password=redis_passwd, charset="utf-8",
                                        decode_responses=True, db=2)
            else:
                self.__db = redis.Redis(host=redis_ip, port=redis_port, password=redis_passwd, charset="utf-8",
                                        decode_responses=True, db=1)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def getOneWait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item

    # 设置字符串
    def setStr(self, name=None, data=None):
        return self.__db.set(name=name, value=data)

    # 获取字符串
    def getStr(self, name):
        return self.__db.get(name=name)

    # 获取字符串
    def delStr(self, name):
        return self.__db.delete(name)