# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.task_private import TaskPrivate
from model.task_private_text import TaskPrivateText
from model.task_private_log import TaskPrivateLog
from model.user_account_group import UserAccountGroup
from model.user_account import UserAccount
import requests
from tools.http import jsonData


class TaskPrivateWork(BaseDao):
    taskId = None
    logId = None
    userId = None
    page = None
    __taskPrivate = None
    __text = None

    def __init__(self, taskId=None, logId=None, userId=None, page=1):
        self.taskId = taskId
        self.logId = logId
        self.userId = userId
        self.page = page

    def addLogData(self, taskId=None):
        self.__taskPrivate = TaskPrivate(guid=taskId)
        data = self.__taskPrivate.byGuidDetails()  # 任务详情

        # 任务文本
        self.__text = TaskPrivateText(task_id=data["guid"])
        textDta = self.__text.byTaskIdDetails()

        # 模糊搜索所有的群成员,带有用户名称的用户进行搜素
        uag = UserAccountGroup(user_id=data["user_id"])
        searchList = uag.handleSearchName(data["soKey"])
        pushNumber = len(searchList)
        # update send number data
        self.__taskPrivate.guid = data["guid"]
        self.__taskPrivate.sendNumber = pushNumber
        self.__taskPrivate.updateSendNumber()

        if pushNumber > 0:
            for v in searchList:
                # print(v["tg_username"])
                try:
                    log = TaskPrivateLog(
                        task_id=data["guid"],
                        user_account_id=v["user_account_id"],
                        user_account_group_user_id=v["user_account_group_id"],
                        soKey=data["soKey"],
                        tg_username=v["tg_username"],
                        tg_user_id=v["tg_user_id"],
                        tg_access_hash=v["tg_access_hash"],
                        tg_nicename=v["tg_nicename"],
                        tg_phone=v["tg_phone"],
                        text=textDta["text"],
                    )
                    log.insert()
                    # print(id)
                except BaseException as err:
                    print(err)

        # print("ok")

    def byTaskIdOne(self):
        self.__taskPrivate = TaskPrivate(guid=self.taskId)
        data = self.__taskPrivate.byGuidDetails()
        return data

    def stop(self):
        self.__taskPrivate = TaskPrivate(guid=self.taskId)
        self.__taskPrivate.stop()

    # 封装发送数据
    def __getSendData(self, acc=None, v=None):
        parameter = {}
        parameter['uid'] = acc.user_id
        parameter['tid'] = acc.guid
        parameter['name'] = acc.api_name
        parameter['apiId'] = acc.api_id
        parameter['apiHash'] = acc.api_hash
        parameter['phone'] = acc.phone
        parameter['proof'] = acc.proof
        parameter['to'] = v.tg_username
        parameter['msg'] = v.text
        parameter['taskId'] = v.task_id
        parameter['logId'] = v.guid
        # print(parameter)
        return parameter

    def checkAcc(self, parameter=None):
        userId = parameter["user_id"]
        taskId = parameter["guid"]
        sendAccountNumber = int(parameter["sendAccountNumber"])
        accountNumber = int(parameter["accountNumber"])

        # 获取发送总数
        sendNumLimit = 1
        if accountNumber == 1:
            sendNumLimit = sendAccountNumber
        else:
            sendNumLimit = accountNumber + sendAccountNumber

        # get send acc number
        acc = UserAccount(user_id=userId)
        accList = acc.getPrivateSendList(limit=accountNumber)

    def builDat(self, parameter=None,taskId=None,sendNumLimit=None,accountNumber=None,accList=None,sendAccountNumber=None):
        # 账号数量
        # 每个账号发送条数
        # 随机抽取账号，根据条数读取数据量，插入队列，队列发起数据
        # print(parameter)
        # user_id  sendAccountNumber accountNumber
        # userId = parameter["user_id"]
        # taskId = parameter["guid"]
        # sendAccountNumber = int(parameter["sendAccountNumber"])
        # accountNumber = int(parameter["accountNumber"])
        #
        # # 获取发送总数
        # sendNumLimit = 1
        # if accountNumber == 1:
        #     sendNumLimit = sendAccountNumber
        # else:
        #     sendNumLimit = accountNumber + sendAccountNumber
        #
        # # get send acc number
        # acc = UserAccount(user_id=userId)
        # accList = acc.getPrivateSendList(limit=accountNumber)

        log = TaskPrivateLog(task_id=taskId)
        ilist = log.getSendList(limit=sendNumLimit)
        # 发送列表
        sendList = []
        try:
            if len(ilist) > 1:
                n = 0
                nacc = 0
                for val in ilist:
                    tmp = {}
                    n += 1
                    if accountNumber == 1:
                        accDat = accList[0]
                        tmp = self.__getSendData(acc=accDat, v=val)
                    else:
                        if n == sendAccountNumber:
                            # 获得当前匹配的发送账号
                            nacc += 1
                            n = 0
                            # 获取当前账号
                            iac = nacc - 1
                            accDat = accList[iac]
                            tmp = self.__getSendData(acc=accDat, v=val)
                    sendList.append(tmp)
                    # 封装发送账号信息
                return sendList
        except BaseException as err:
            print("builDat:", err)

        return sendList

    def sendOk(self, logId=None):
        log = TaskPrivateLog()
        return log.sendOk(guid=logId)

    # 删除定时任务
    def delApsJob(self, taskId=None):
        json = {'id': taskId}
        r = requests.get('http://127.0.0.1:9896/private/del', params=json)
        if r.status_code:
            return True
        return False

    def checkTask(self, sendNumber=None):
        log = TaskPrivateLog(task_id=self.taskId)
        count = log.getByTaskIdCount()
        if count == sendNumber:
            task = TaskPrivate(guid=self.taskId)
            task.finish()
            return True
        else:
            return False
