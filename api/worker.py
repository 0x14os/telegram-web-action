#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import redis

from rq import Worker, Queue, Connection
from config.conf import redis_ip, redis_port, redis_passwd

from tg.tg import Tg
from tg.personal import Personal
from tg.group import Group
from tg.channel import Channel

from dao.task_dao import TaskDao
from model.user_account import UserAccount
from model.task import Task

from works.task_private_works import TaskPrivateWork
from works.me_works import MeWorks
from works.msg_works import MsgWorks

from tools.do import Do
from tools.help import getTime, toDate

import time

rootDir = os.path.abspath(os.path.dirname(__file__))
do = Do()

listen = ['default']
conn = redis.Redis(host=redis_ip, port=redis_port, password=redis_passwd)


def runWorker(parameter=None):  # 任务

    try:
        print(parameter)
        _func = parameter["func"]
        _parameter = parameter["parameter"]
        _ext = parameter["ext"]
        # print("parameter: {} and type: {}".format(parameter, type(parameter)))
        # print(_ext['jobId'])

        cf = _func.split(".")
        # print(cf)
        classNmae = cf[0]
        classFunc = cf[1]
        response = {}
        if classNmae == "account":
            # print(classFunc)
            response = account(classFunc, _parameter)
        elif classNmae == "group":
            response = group(classFunc, _parameter)
        elif classNmae == "personal":
            response = personal(classFunc, _parameter)
        elif classNmae == "taskPrivate":
            response = taskPrivate(classFunc, _parameter)
        elif classNmae == "channel":
            response = channel(classFunc, _parameter)
        elif classNmae == "noTgInfo":
            response = noTgInfo(classFunc, _parameter)
        elif classNmae == "auto":
            response = auto(classFunc, _parameter)
        return response
    except BaseException as err:
        print(err)


def auto(func=None, parameter=None):
    if func == "checkAccount":
        print("checkAccount")
        if parameter["uid"] != None:
            me = MeWorks()
            me.batchCheckAcc(uid=parameter["uid"], rootDir=rootDir)
            msg = MsgWorks(userId=parameter["uid"])
            msg.checkAccount()
        # print(1212)
    return True


def account(func=None, parameter=None):  # 账号
    tid = parameter['tid']
    itg = Tg()
    itg.rootDir = rootDir
    itg.iname = parameter['name']
    itg.api_id = parameter['apiId']
    itg.api_hash = parameter['apiHash']
    itg.iphone = parameter['phone']
    itg.proof = parameter['proof']
    msg = MsgWorks(userId=parameter["uid"])

    if func == "code":  # 发送验证码
        print("code")
        cmdSta = itg.webLoginPushCode(tid=tid)
        print("cmdSta:", cmdSta)
        if cmdSta:
            msg.code()
            return do.ok()

    elif func == "login":  # 登陆
        icode = parameter['code']
        phoneHash = parameter['phoneHash']
        if isinstance(icode, int):
            print(icode, tid, phoneHash)
            cmdSta = itg.cmdLogin(code=icode, tid=tid, phash=phoneHash)
        if cmdSta:
            msg.login()
            return do.ok()
    return do.error()


def channel(func=None, parameter=None):
    channel = Channel()
    channel.rootDir = rootDir
    channel.iname = parameter['name']
    channel.api_id = parameter['apiId']
    channel.api_hash = parameter['apiHash']
    channel.iphone = parameter['phone']
    channel.proof = parameter['proof']
    channel.init()
    msg = MsgWorks(userId=parameter["uid"])
    if func == "joinNGroup":
        print("自动加群")
        channel.joinNGroup(usernName=parameter["groupLink"])
        msg.joinNGroup()
        return do.ok()


def noTgInfo(func=None, parameter=None):
    try:
        # 定时群发
        if func == "pushMsgMultiple":
            print("pushMsgMultiple")
            taskId = parameter["taskId"]
            task = TaskDao(taskId=taskId)
            list = task.byTaskIdMsgList()
            # print(list)
            if len(list) > 0:
                for v in list:
                    # print(v)
                    group = Group()
                    group.rootDir = rootDir
                    group.iname = v["apiName"]
                    group.api_id = v["apiId"]
                    group.api_hash = v["apiHash"]
                    group.iphone = v["phone"]
                    group.proof = v["proof"]
                    group.init()
                    group.to = v["to"]
                    group.msg = v["msg"]
                    group.pushOneMsg()

    except BaseException as err:
        print(err)

    return do.ok()


def group(func=None, parameter=None):  # 群组
    group = Group()
    group.rootDir = rootDir
    group.iname = parameter['name']
    group.api_id = parameter['apiId']
    group.api_hash = parameter['apiHash']
    group.iphone = parameter['phone']
    group.proof = parameter['proof']
    group.init()
    msg = MsgWorks(userId=parameter["uid"])
    if func == "getGroup":  # 获取账号下的群
        print("获取账号下的群")
        uid = parameter['uid']
        tid = parameter['tid']
        list = group.getGroup(user_id=uid, user_account_id=tid)
        msg.getGroup(tid=tid)
        return do.ok(idata=list)

    elif func == "getExtractGroup":  # 获取指定群成员信息
        print("获取指定群成员信息")
        tgid = parameter['tgid']
        group.getExtractGroup(tgid=tgid)
        msg.getExtractGroup(tid=parameter['tid'], tgid=tgid)
        return do.ok()

    elif func == "pushOneMsg":  # 推送n条信息到群
        group.to = parameter['to']
        group.msg = parameter['msg']
        group.pushOneMsg()
        return do.ok(idata=group.result())

    elif func == "pushMsg":
        taskId = parameter["taskId"]
        tas = Task(guid=taskId)
        tshow = tas.byGuidDetails()
        group.to = parameter['to']
        group.msg = tshow["msg"]
        group.pushOneMsg()
        return do.ok(idata=group.result())

    elif func == "newGroup":
        tid = parameter['tid']
        ua = UserAccount(guid=tid)
        uaShow = ua.byGuidDetails()
        group.newName = uaShow["new_group_name"]
        new_group_list = []
        if uaShow["new_group_list"]:
            new_group_list = uaShow["new_group_list"].split(",")
        group.userNameList = new_group_list
        group.newGroup()
        sta = None
        if group.result():
            sta = ua.upNewGroup(is_new_group=1)
        else:
            sta = ua.upNewGroup(is_new_group=3)
        if sta:
            msg.newGroup(tid=tid)
            return do.ok()

    return do.error()


def personal(func=None, parameter=None):  # 私人
    per = Personal()

    per.rootDir = rootDir
    per.iname = parameter['name']
    per.api_id = parameter['apiId']
    per.api_hash = parameter['apiHash']
    per.iphone = parameter['phone']
    per.proof = parameter['proof']

    per.init()

    if func == "pushMsg":  # 推送消息
        per.to = parameter['to']
        per.msg = parameter['msg']
        per.pushMsg()
        return do.ok(idata=per.result())

    elif func == "privateLetter":  # 私信
        print(121212)

    return do.ok()


# 私有任务导入发送名单
def taskPrivate(func=None, parameter=None):
    # print("works print:")
    # print(toDate(getTime()))
    # print(parameter)
    if func == "addLogData":
        msg = MsgWorks(userId=parameter["uid"])
        taskId = parameter["taskId"]
        dao = TaskPrivateWork()
        dao.addLogData(taskId=taskId)
        # 导入完成，通知
        msg.taskPrivateAddLogData(taskId=taskId)

    elif func == "push":
        try:

            userId = parameter["user_id"]
            taskId = parameter["guid"]
            # insufficientPrivateMessageAccount
            work = TaskPrivateWork(taskId=taskId)
            msg = MsgWorks(userId=userId)

            sendAccountNumber = int(parameter["sendAccountNumber"])
            accountNumber = int(parameter["accountNumber"])
            sendNumber = int(parameter["sendNumber"])
            sendNumLimit = 1
            if accountNumber == 1:
                sendNumLimit = sendAccountNumber
            else:
                sendNumLimit = accountNumber + sendAccountNumber
            # check task
            isCheck = work.checkTask(sendNumber=sendNumber)
            if isCheck == False:
                # check tg acc
                me = MeWorks()
                me.batchCheckAcc(uid=userId, rootDir=rootDir)

                acc = UserAccount(user_id=userId)
                accList = acc.getPrivateSendList(limit=accountNumber)
                if len(accList) >= 1:
                    sendList = work.builDat(taskId=taskId, sendNumLimit=sendNumLimit, accountNumber=accountNumber,
                                            accList=accList, sendAccountNumber=sendAccountNumber)
                    if len(sendList) > 1:
                        for val in sendList:
                            personal(func="pushMsg", parameter=val)
                            work.sendOk(logId=val["logId"])
                            time.sleep(2)
                else:
                    # update data status
                    work.stop()
                    # del job task
                    work.delApsJob(taskId=taskId)
                    # Notice user
                    msg.insufficientPrivateMessageAccount()
            else:
                work.delApsJob(taskId=taskId)
                # Notice user
                msg.privateMessageTaskIsOver()

        except BaseException as err:
            print("taskPrivate:", err)

    return do.ok()


if __name__ == '__main__':
    with Connection(conn):  # 建立与redis server的连接
        worker = Worker(list(map(Queue, listen)))  # 建立worker监听给定的队列
        worker.work()
