# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from model.task import Task
from model.user_account import UserAccount
from model.user_account_group import UserAccountGroup


class TaskMsg(db.Model):
    __tablename__ = 'tg_task_msg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(38))
    user_account_group_id = db.Column(db.String(38), unique=False, index=True)
    text = db.Column(db.String)
    status = db.Column(db.Integer, default=1)
    status_time = db.Column(db.Integer, default=10)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)
    addAll = None

    iPage = 1

    def __init__(self, addAll=None, task_id=None, user_account_group_id=None, text=None, status_time=0,
                 status=1, page=1):
        self.addAll = addAll
        self.task_id = task_id
        self.user_account_group_id = user_account_group_id
        self.text = text
        self.status_time = status_time
        self.status = status
        self.iPage = page

    def insertAll(self):
        db.session.add_all(self.addAll)
        return db.session.commit()

    def insert(self):
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        return db.session.commit()

    def update(self):
        data = {}
        data["update_time"] = getTime()
        user = TaskMsg.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                db.session.commit()
                return True
        return False

    def delete(self):
        msg = TaskMsg.query.filter_by(task_id=self.task_id).delete()
        if msg is not None:
            db.session.commit()
            return True
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["status_time"] = self.status_time
        data["status_exp_log"] = self.status_exp_log
        data["update_time"] = getTime()
        user = TaskMsg.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                db.session.commit()
                return True
        return False

    def byListPage(self):
        db.session.commit()
        u = TaskMsg.query.filter_by(status=self.status).paginate(page=1, per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    # join双表查询
    def byTaskIdList(self):
        db.session.commit()
        query = db.session.query(TaskMsg, UserAccountGroup).filter(
            TaskMsg.user_account_group_id == UserAccountGroup.guid).order_by(
            TaskMsg.id.desc()).all()

        tmp = []
        # groupName text id
        if len(query) >= 1:
            for val in query:
                imap = {}
                imap["id"] = val.TaskMsg.id
                imap["groupName"] = val.UserAccountGroup.channel_title
                imap["text"] = val.TaskMsg.text
                imap["create_time"] = toDate(val.TaskMsg.create_time)
                imap["update_time"] = toDate(val.TaskMsg.update_time)
                tmp.append(imap)
        return tmp

    def jobMsg(self):
        db.session.commit()
        query = db.session.query(TaskMsg, Task, UserAccount, UserAccountGroup).filter(
            TaskMsg.task_id == Task.guid).filter(
            Task.user_account_id == UserAccount.guid).filter(
            TaskMsg.user_account_group_id == UserAccountGroup.guid).filter(Task.status == 1).order_by(
            TaskMsg.id.desc()).all()
        tmp = []
        if len(query) >= 1:
            for val in query:
                imap = {}
                imap["id"] = val.TaskMsg.id
                imap["method"] = val.Task.method
                imap["apiId"] = val.UserAccount.api_id
                imap["apiHash"] = val.UserAccount.api_hash
                imap["apiName"] = val.UserAccount.api_name
                imap["to"] = val.UserAccountGroup.channel_id
                imap["msg"] = val.Task.msg
                imap["timer"] = val.Task.timer
                imap["taskStatus"] = val.TaskMsg.status
                tmp.append(imap)
        return tmp

    # 根据任务id查询
    def byTaskIdMsgList(self):
        db.session.commit()
        query = db.session.query(TaskMsg, Task, UserAccount, UserAccountGroup).filter(
            TaskMsg.task_id == Task.guid).filter(
            Task.user_account_id == UserAccount.guid).filter(
            TaskMsg.user_account_group_id == UserAccountGroup.guid).filter_by(
            task_id=self.task_id).order_by(
            TaskMsg.id.desc()).all()
        tmp = []
        if len(query) >= 1:
            for val in query:
                imap = {}
                imap["phone"] = val.UserAccount.phone
                imap["proof"] = val.UserAccount.proof
                imap["method"] = val.Task.method
                imap["apiId"] = val.UserAccount.api_id
                imap["apiHash"] = val.UserAccount.api_hash
                imap["apiName"] = val.UserAccount.api_name
                imap["id"] = val.TaskMsg.id
                imap["to"] = val.UserAccountGroup.channel_id
                imap["msg"] = val.Task.msg
                imap["timer"] = val.Task.timer
                imap["taskStatus"] = val.TaskMsg.status

                tmp.append(imap)
        return tmp

    # 根据任务id查询所有的消息id
    def byTaskIdMsgIdList(self):
        db.session.commit()
        query = TaskMsg.query.filter_by(task_id=self.task_id).all()
        tmp = []
        if len(query) >= 1:
            for val in query:
                imap = {}
                imap["id"] = val.id
                tmp.append(imap)
        return tmp

    # 根据id查询一条
    def byIdMsgOne(self):
        db.session.commit()
        val = db.session.query(TaskMsg, Task, UserAccount, UserAccountGroup).filter(
            TaskMsg.task_id == Task.guid).filter(
            Task.user_account_id == UserAccount.guid).filter(
            TaskMsg.user_account_group_id == UserAccountGroup.guid).filter(Task.status == 1).filter_by(
            id=TaskMsg.id).first()
        if val:
            imap = {}
            imap["id"] = val.TaskMsg.id
            imap["method"] = val.Task.method
            imap["apiId"] = val.UserAccount.api_id
            imap["apiHash"] = val.UserAccount.api_hash
            imap["apiName"] = val.UserAccount.api_name
            imap["to"] = val.UserAccountGroup.channel_id
            imap["msg"] = val.Task.msg
            imap["timer"] = val.Task.timer
            imap["taskStatus"] = val.TaskMsg.status
            return imap
        return False

    # 根据任务id 删除全部消息
    def byTaskIdDel(self, status=2):
        data = {}
        data["status"] = status
        data["update_time"] = getTime()
        result = TaskMsg.query.filter_by(task_id=self.task_id).update(data)
        if result is not None:
            db.session.commit()
            return True
        return False

    # 根据消息id 删除全部消息
    def byMsgIdDel(self):
        TaskMsg.query.filter(TaskMsg.id == self.id).delete()
        db.session.commit()
        return True

    def byGuidDel(self):
        TaskMsg.query.filter(TaskMsg.task_id == self.task_id).delete()
        db.session.commit()
        return True
