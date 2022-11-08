# !/usr/bin/env python
# -*- coding:utf-8 -*-
from dao.base_dao import BaseDao
from model.msg import Msg
from tools.help import jsonDumps


class MsgWorks(BaseDao):
    msgId = None
    userId = None

    def __init__(self, userId=None):
        self.userId = userId

    def __addMsg(self, uid=None, title=None, text=None):
        ob = Msg(user_id=uid, title=title, text=text)
        ob.insert()

    def __getData(self, id=None, text=None, uri=None, ext=None):
        dat = {}
        dat['id'] = id
        dat['text'] = text
        dat['uri'] = uri
        dat['ext'] = ext
        return jsonDumps(dat)



    def autoCheckAccount(self):
        text = self.__getData(uri="/account/list", text="自动触发账号检测")
        self.__addMsg(uid=self.userId, title="TG账号检测完毕", text=text)


    # 自动检测账号
    def checkAccount(self):
        text = self.__getData(uri="/account/list", text="请点击查阅账号列表.")
        self.__addMsg(uid=self.userId, title="TG账号检测完毕", text=text)

    # 获取登录code
    def code(self):
        text = self.__getData(uri="/account/list", text="请点击查阅,该账号已发送code")
        self.__addMsg(uid=self.userId, title="已发送code", text=text)

    # 登录tg
    def login(self):
        text = self.__getData(uri="/account/list", text="请点击查阅,该账号已激活")
        self.__addMsg(uid=self.userId, title="账号已激活", text=text)

    def joinNGroup(self):
        text = self.__getData(uri="/account/group/list/0", text="请点击查阅,自动加群完毕")
        self.__addMsg(uid=self.userId, title="自动加群完毕", text=text)

    # 间隔群发消息
    def pushMsgMultiple(self):
        print(1111)

    # 获取账号下的群
    def getGroup(self, tid=None):
        text = self.__getData(uri="/account/group/list/" + tid, text="请点击查阅,获取群列表完毕")
        self.__addMsg(uid=self.userId, title="获取群列表完毕", text=text)

    # 获取群成员
    def getExtractGroup(self, tid=None, tgid=None):
        text = self.__getData(uri="/account/group/user/" + tid + "/" + tgid, text="请点击查阅,获取群成员完毕")
        self.__addMsg(uid=self.userId, title="获取群成员完毕", text=text)


    # 推送一条群信息
    def pushOneMsg(self):
        print("is not")

    # 推送群信息
    def pushMsg(self):
        print(1111)

    # 新建一个群
    def newGroup(self,tid=None):
        text = self.__getData(uri="/account/group/list/" + tid , text="请点击查阅,新建群完毕")
        self.__addMsg(uid=self.userId, title="新建群完毕", text=text)

    # 发送一条私人信息
    def personalPushMsg(self):
        print(1111)

    # 导入待发送的私信名单
    def taskPrivateAddLogData(self,taskId=None):
        text = self.__getData(uri="/private/log/" + taskId, text="请点击查阅,私信发送名单导入完毕")
        self.__addMsg(uid=self.userId, title="私信发送名单导入完毕", text=text)

    # taskPrivateSend is not msg
    def taskPrivatePushMsg(self):
        print(1111)

    # Insufficient private message account /private/list
    def insufficientPrivateMessageAccount(self):
        text = self.__getData(uri="/private/list", text="请点击查阅,私信TG账号不足")
        self.__addMsg(uid=self.userId, title="私信TG账号不足", text=text)

    # Private message task is over
    def privateMessageTaskIsOver(self):
        text = self.__getData(uri="/private/list", text="请点击查阅,私信结束")
        self.__addMsg(uid=self.userId, title="私信结束", text=text)