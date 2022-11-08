# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate


class TaskPrivateLog(db.Model):
    __tablename__ = 'tg_task_private_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    task_id = db.Column(db.String(38))
    user_account_id = db.Column(db.String(38))
    user_account_group_user_id = db.Column(db.String(38))
    soKey = db.Column(db.String(30))
    tg_username = db.Column(db.String(180))
    tg_user_id = db.Column(db.String(180))
    tg_access_hash = db.Column(db.String(180))
    tg_nicename = db.Column(db.String(180))
    tg_phone = db.Column(db.String(180))
    text = db.Column(db.Text)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)
    iPage = 1

    def __init__(self, guid=None, task_id=None, user_account_id=None, user_account_group_user_id=None, soKey=None,
                 tg_username=None, tg_user_id=None, tg_access_hash=None, tg_nicename=None, tg_phone=None, text=None,
                 status=1,
                 page=1):
        self.guid = guid
        self.task_id = task_id
        self.user_account_id = user_account_id
        self.user_account_group_user_id = user_account_group_user_id
        self.tg_username = tg_username
        self.tg_user_id = tg_user_id
        self.tg_access_hash = tg_access_hash
        self.tg_nicename = tg_nicename
        self.tg_phone = tg_phone
        self.soKey = soKey
        self.text = text
        self.status = status
        self.iPage = page

    def getDictionary(self):
        data = {}
        data["guid"] = self.guid
        data["task_id"] = self.task_id
        data["user_account_id"] = self.user_account_id
        data["user_account_group_user_id"] = self.user_account_group_user_id
        data["tg_username"] = self.tg_username
        data["tg_user_id"] = self.tg_user_id
        data["tg_access_hash"] = self.tg_access_hash
        data["tg_nicename"] = self.tg_nicename
        data["tg_phone"] = self.tg_phone
        data["soKey"] = self.soKey
        data["text"] = self.text
        data["status"] = self.status
        return data

    def insert(self):
        self.guid = str(getGuid())
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        if db.session.commit() == None:
            return self.guid
        else:
            return False

    def update(self):
        data = {}
        data["text"] = self.text
        data["update_time"] = getTime()
        user = TaskPrivateLog.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = TaskPrivateLog.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def byListPage(self):
        db.session.commit()
        u = TaskPrivateLog.query.filter_by(task_id=self.task_id).order_by(TaskPrivateLog.id.desc()).paginate(
            page=self.iPage,
            per_page=30)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byGuidDetails(self):
        db.session.commit()
        d = TaskPrivateLog.query.filter_by(guid=self.guid).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["task_id"] = d.task_id
            detail["text"] = d.text
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None

    def getTaskListNotPage(self):
        db.session.commit()
        list = TaskPrivateLog.query.filter_by(status=1).all()
        if len(list) >= 1:
            dictList = dictToListJoinDict(list)
            return dictList
        return False

    def byGuidDel(self):
        stu = TaskPrivateLog.query.filter(TaskPrivateLog.task_id == self.task_id).delete()
        stuDel = db.session.commit()
        print(stu)
        print(stuDel)

    def getSendList(self, limit=0):
        db.session.commit()
        ilist = TaskPrivateLog.query.filter_by(task_id=self.task_id, status=1).order_by(TaskPrivateLog.id.desc()).limit(
            limit).all()
        return ilist

    def sendOk(self, guid=None):
        data = {}
        data["status"] = 2
        data["update_time"] = getTime()
        TaskPrivateLog.query.filter_by(guid=guid).update(data)
        db.session.commit()
        return True

    def getByTaskIdCount(self):
        db.session.commit()
        count = TaskPrivateLog.query.filter_by(task_id=self.task_id).filter_by(status=2).count()
        if count:
            return count
        return 0
