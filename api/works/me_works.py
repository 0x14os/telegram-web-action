# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.user_account import UserAccount
from tg.me import Me

import time


class MeWorks(BaseDao):

    # 批量检查账号
    def batchCheckAcc(self, uid=None, rootDir=None):
        if uid != None or rootDir != None:
            try:
                ua = UserAccount()
                ilist = ua.byUserIdAutoList(userId=uid)
                if len(ilist) > 0:
                    for v in ilist:
                        # print(v)
                        if v['proof'] != None:
                            me = Me()
                            me.rootDir = rootDir
                            me.api_id = v['api_id']
                            me.api_hash = v['api_hash']
                            # self.iphone = v['phone']
                            me.proof = v['proof']
                            me.init()
                            stu = me.client.get_me()
                            # print(stu)
                            if stu is None:
                                ua.byUpTidStatusInvalid(tid=v["guid"])
                        time.sleep(1)
            except BaseException as err:
                print(err)

    # 检测账号
    def autoCheck(self, status=None, tid=None):
        ua = UserAccount()
        if status is None:
            ua.byUpTidStatusInvalid(tid=tid)
            return True
        return False
