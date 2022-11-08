# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.task_private import TaskPrivate
from model.task_private_text import TaskPrivateText
from model.task_private_log import TaskPrivateLog
from model.user_account_group import UserAccountGroup
import requests
from tools.http import jsonData


class TaskPrivateDao(BaseDao):
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

        self.__taskPrivate = TaskPrivate()
        self.__text = TaskPrivateText()
        # self.__log = TaskPrivateLog()


    def getTaskPrivateList(self):
        self.__taskPrivate.user_id = self.userId
        self.__taskPrivate.iPage = self.page
        list = self.__taskPrivate.byListPage()
        return list


    def getTaskPrivateListLog(self):
        log = TaskPrivateLog(task_id=self.taskId)
        log.iPage = self.page
        list = log.byListPage()
        return list


    # add this task data
    def addTaskPrivate(self, data={}):
        try:
            self.__taskPrivate.user_id = data["user_id"]
            pushText = data["text"]
            data["userAccountIdList"] = ""
            # 群发数量 根据实际检索出的发送数量计算获得
            self.__taskPrivate.sendNumber = 0
            self.__taskPrivate.userAccountIdList = data["userAccountIdList"]
            # 待发送数量
            self.__taskPrivate.sendAccountNumber = int(data["sendAccountNumber"])
            self.__taskPrivate.accountNumber = int(data["accountNumber"])
            self.__taskPrivate.soKey = data["soKey"]
            self.__taskPrivate.remark = data["remark"]
            self.__taskPrivate.timer = int(data["timer"])  # 休眠时间 默认5秒
            self.__taskPrivate.title = data["title"]

            taskId = self.__taskPrivate.insert()

            if taskId != False:
                self.__text.task_id = taskId
                self.__text.text = pushText
                textId = self.__text.insert()
                if textId != False:
                    return taskId
        except BaseException as err:
            print(err)
        return False


    # edit this task data
    def editTaskPrivate(self, data={}):
        self.__taskPrivate.guid = data["guid"]
        self.__taskPrivate.title = data["title"]
        print(type(data["remark"]))
        if type(data["remark"]) == None:
            self.__taskPrivate.remark = ""
        else:
            self.__taskPrivate.remark = data["remark"]

        if int(data["timer"]) == 0:
            self.__taskPrivate.timer = int(data["timer"])  # 休眠时间 默认5秒
        else:
            self.__taskPrivate.timer = 5
        stu = self.__taskPrivate.edit()
        return stu

    def delAll(self):
        self.__taskPrivate.guid = self.taskId
        self.__taskPrivate.byGuidDel()
        self.__text.task_id = self.taskId
        self.__text.byGuidDel()
        log = TaskPrivateLog()
        log.task_id = self.taskId
        log.byGuidDel()
        # 删除任务
        self.delApsJob()
        return True

    def getOne(self):
        self.__taskPrivate.guid = self.taskId
        data = self.__taskPrivate.byGuidDetails()
        self.__text.task_id = self.taskId
        textDat = self.__text.byTaskIdDetails()
        data["text"] = ""
        if len(data) > 0 or len(textDat) > 0:
            data["text"] = textDat["text"]
        return data

    def stopTask(self):
        self.__taskPrivate.guid = self.taskId
        self.__taskPrivate.stop()
        # 删除任务
        self.delApsJob()
        return True

    def startTask(self):
        self.__taskPrivate.guid = self.taskId
        self.__taskPrivate.start()
        self.addApsJob()
        return True

    # 增加定时任务
    def addApsJob(self):
        json = {'id': self.taskId}
        r = requests.get('http://127.0.0.1:9896/private/add', params=json)
        if r.status_code:
            return True
        return False

    # 删除定时任务
    def delApsJob(self):
        json = {'id': self.taskId}
        r = requests.get('http://127.0.0.1:9896/private/del', params=json)
        if r.status_code:
            return True
        return False

