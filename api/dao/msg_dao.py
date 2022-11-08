# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.msg import Msg


class MsgDao(BaseDao):
    msgId = None
    userId = None

    def __init__(self, msgId=None, userId=None):
        self.msgId = msgId
        self.userId = userId

    def getUserIdList(self):
        ob = Msg(user_id=self.userId)
        return ob.byUserIdList()

    def getUserIdCountAOne(self):
        ob = Msg(user_id=self.userId)
        count = ob.byUserIdCount()
        dat = ob.byUserIdOne()
        tmp = {}
        tmp['count'] = count
        tmp['dat'] = dat
        return tmp

    def byGuidReadUp(self):
        ob = Msg(guid=self.msgId)
        ob.upStatus()
        return True

