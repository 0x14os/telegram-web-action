# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.user_account import UserAccount
from tools.help import getGuid


class JobRq():
    uid = None
    tid = None
    uaDetails = {}
    __parameter = {}

    def __init__(self, uid=None, tid=None):
        self.uid = uid
        self.tid = tid

    def ___getUserAccountDetails(self):
        utg = UserAccount(user_id=self.uid, guid=self.tid)
        data = utg.byGuidDetails()
        if data:
            self.uaDetails = data

    #  get job id
    def __getJobId(self):
        return str(getGuid())

    # 获取验证码
    def getCode(self, uid=None, tid=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'account.code'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": self.uaDetails["phone"],
            "proof": self.uaDetails["proof"]
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 登陆验证
    def webActivationLogin(self, code=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'account.login'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
            "phoneHash": self.uaDetails["phone_code_hash"],
            "code": code
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 获取群
    def getGroup(self):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'group.getGroup'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 提取群成员
    def getExtractGroup(self, tgGroupId=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'group.getExtractGroup'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
            "tgid": tgGroupId,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 发送一条信息到群里
    def pushGroupOneMsg(self, to=None, msg=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'group.pushOneMsg'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
            "to": int(to),
            "msg": msg,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 发送一条信息到群里
    def apsPushGroupOneMsg(self, apiName=None, apiId=None, apiHash=None, to=None, msg=None, msgId=None):
        proof = "/session/" + apiName
        self.__parameter["func"] = 'group.pushOneMsg'
        self.__parameter["parameter"] = {
            "uid": self.uid,
            "proof": proof,
            "name": apiName,
            "apiId": int(apiId),
            "apiHash": apiHash,
            "phone": str("0000000"),
            "to": int(to),
            "msg": msg,
            "msgId": msgId,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 多个群推送信息
    def pushMsgGroupMultiple(self, taskId=None):
        self.__parameter["func"] = 'noTgInfo.pushMsgMultiple'
        self.__parameter["parameter"] = {
            "uid": self.uid,
            "taskId": taskId,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 发送一条信息到某个人
    def pushPrivateOneMsg(self, to=None, msg=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'personal.pushMsg'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
            "to": to,
            "msg": msg,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    def newGroup(self):  # 新建群
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'group.newGroup'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    #   私有任务导入发送名单
    def taskPrivate(self, taskId=None):
        # self.___getUserAccountDetails()
        self.__parameter["func"] = 'taskPrivate.addLogData'
        self.__parameter["parameter"] = {
            "uid": self.uid,
            "taskId": taskId,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    #  aps 私有任务发送,not msg
    def taskPrivateSend(self, parameter=None):
        # self.___getUserAccountDetails()
        self.__parameter["func"] = 'taskPrivate.push'
        self.__parameter["parameter"] = parameter
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 自动加群
    def joinGroup(self, groupLink=None):
        self.___getUserAccountDetails()
        self.__parameter["func"] = 'channel.joinNGroup'
        self.__parameter["parameter"] = {
            "tid": self.tid,
            "uid": self.uid,
            "proof": self.uaDetails["proof"],
            "name": self.uaDetails["api_name"],
            "apiId": int(self.uaDetails["api_id"]),
            "apiHash": self.uaDetails["api_hash"],
            "phone": str("+" + self.uaDetails["phone"]),
            "groupLink": groupLink,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter

    # 批量检测账号
    def checkAccount(self):
        self.__parameter["func"] = 'auto.checkAccount'
        self.__parameter["parameter"] = {
            "uid": self.uid,
        }
        self.__parameter["ext"] = {
            "jobId": self.__getJobId()
        }
        return self.__parameter
