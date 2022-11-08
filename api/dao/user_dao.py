# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao

from model.task_msg import TaskMsg
from model.task import Task
from model.user_account import UserAccount
from model.user import User

from dao.task_dao import TaskDao

from tools.redis_con import RedisCon
from tools.passwd import checkPasswd
from tools.help import md5, getGuid
from job.job_rq import JobRq
import random
import json


class UserDao(BaseDao):
    taskId = None
    msgId = None
    userId = None
    __task = None
    __msg = None
    __ua = None
    __user = None

    def __init__(self, taskId=None, msgId=None, userId=None):
        self.taskId = taskId
        self.msgId = msgId
        self.userId = userId

    def login(self, email=None, passwd=None, remote_addr=None, ruser=None):
        # 新建队列名为rq
        # ruser = RedisCon('user')
        u = User(email=email)
        d = u.byEmailDetails()
        if d == False:
            return False

        oldPasswd = passwd + str(d["password_random"])
        is_check = checkPasswd(d["password"], oldPasswd)

        if is_check == True:
            tokenStr = getGuid()
            setNumTop = random.randrange(0, 101, 20)
            tokenStr = str(tokenStr) + str(setNumTop)
            token = md5(tokenStr)

            if d["login_count"] != None:
                icount = d["login_count"]
            else:
                icount = 1

            login_count = int(icount) + 1
            last_ip = remote_addr
            user = User(guid=d["guid"], token=token, last_ip=last_ip, login_count=login_count)
            if user.upLoginToken() == None:
                ua = UserAccount(user_id=d['guid'])
                tgCount = ua.byUserIdTgCount()
                task = Task(user_id=d['guid'])
                taskCount = task.byUserIdTaskCount()

                loginData = {}
                loginData["user_id"] = d["guid"]
                loginData["token"] = token
                loginData["role"] = d["role_use"]
                loginData["tgCount"] = tgCount
                loginData["taskCount"] = taskCount
                if d["taskNumber"] == None:
                    loginData["taskNumber"] = 0
                else:
                    loginData["taskNumber"] = d["taskNumber"]

                if d["tgNumber"] == None:
                    loginData["tgNumber"] = 0
                else:
                    loginData["tgNumber"] = d["tgNumber"]

                if d["tgGroupNumber"] == None:
                    loginData["tgGroupNumber"] = 0
                else:
                    loginData["tgGroupNumber"] = d["tgGroupNumber"]

                loginData["tgStatus"] = 1
                loginData["taskStatus"] = 1

                if d["role_use"] == 2:
                    if tgCount >= loginData["tgNumber"]:
                        loginData["tgStatus"] = 2

                    if taskCount >= loginData["taskNumber"]:
                        loginData["taskStatus"] = 2

                cacheData = json.dumps(loginData)
                ruser.setStr(name=token, data=cacheData)
                return loginData

    # 批量导入协议号
    def loadAddAcc(self, phone=None):
        proof = "/session/" + phone
        ua = UserAccount(user_id=self.userId, api_name=phone, api_id=4, api_hash="014b35b6184100b085b0d0572f9b5103",
                         phone=phone,
                         username=phone, is_activation=2, is_group=1, is_new_group=1, mode=2, proof=proof)
        ua.insert()
        return True

    # 自动加入
    def joinGroup(self, tid=None,uid=None,groupLink=[]):
        job = JobRq(tid=tid,uid=uid)
        return job.joinGroup(groupLink=groupLink)



    def checkAccount(self, uid=None,):
        job = JobRq(uid=uid)
        return job.checkAccount()



