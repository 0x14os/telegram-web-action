# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.task_msg import TaskMsg
from model.task import Task
import requests
from tools.http import jsonData


class TaskDao(BaseDao):
    taskId = None
    msgId = None
    userId = None
    __task = None
    __msg = None

    def __init__(self, taskId=None, msgId=None, userId=None):
        self.taskId = taskId
        self.msgId = msgId
        self.userId = userId

    def getTaskDetails(self):
        task = Task(guid=self.taskId)
        dat = task.byGuidDetails()
        return dat

    def addTask(self, data=None):
        try:
            user_account_group_list = data["user_account_group_list"]
            group_list = user_account_group_list.split(",")
            send_group_number = len(group_list)
            timer = data["timer"]
            method = data["method"]

            model = Task(
                method=method,
                user_account_group_list=data["user_account_group_list"],
                send_group_number=send_group_number,
                title=data["title"],
                msg=data["msg"],
                remark=data["remark"],
                timer=timer)

            if data["guid"] == 0:
                model.user_id = data["user_id"]
                model.user_account_id = data["user_account_id"]
                taskId = model.insert()
                if taskId != False:
                    for group_id in group_list:
                        maddAll = TaskMsg(task_id=taskId, user_account_group_id=group_id, text=data["msg"])
                        maddAll.insert()
            return True
        except BaseException as err:
            return err

    # 删除任务和消息
    def byTaskIdInUidDelMsg(self):
        self.__task = Task()
        self.__msg = TaskMsg()
        # self.__task.user_id = self.userId
        self.__task.guid = self.taskId
        self.__task.byGuidDel()
        self.__msg.task_id = self.taskId
        self.__msg.byGuidDel()
        return True

    # 删除消息
    def byMsfIdMsgDel(self, msgId=None):
        self.__task = Task()
        self.__msg = TaskMsg()
        self.__msg.id = msgId
        self.__msg.byMsgIdDel()
        return True

    # 根据任务id查询消息列表
    def byTaskIdMsgList(self):
        # self.__task = Task()
        self.__msg = TaskMsg()
        self.__msg.task_id = self.taskId
        return self.__msg.byTaskIdMsgList()

    def start(self):
        self.__task = Task(guid=self.taskId)
        self.__task.start()
        self.__addApsJob()
        return True

    def stop(self):
        self.__task = Task(guid=self.taskId)
        self.__task.stop()
        self.__delApsJob()
        return True

    # 增加定时任务
    def __addApsJob(self):
        json = {'id': self.taskId}
        r = requests.get('http://127.0.0.1:9896/group/add', params=json)
        if r.status_code:
            return True
        return False

    # 删除定时任务
    def __delApsJob(self):
        json = {'id': self.taskId}
        r = requests.get('http://127.0.0.1:9896/group/del', params=json)
        if r.status_code:
            return True
        return False
