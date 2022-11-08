# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate


class TaskPrivateText(db.Model):
    __tablename__ = 'tg_task_private_text'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    task_id = db.Column(db.String(38), unique=False, index=True)
    text = db.Column(db.Text)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)
    iPage = 1

    def __init__(self, guid=None, task_id=None, text=None, status=1,
                 page=1):
        self.guid = guid
        self.task_id = task_id
        self.text = text
        self.status = status
        self.iPage = page

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
        user = TaskPrivateText.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = TaskPrivateText.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # 删除
    def byGuidInUidDel(self, status=2):
        data = {}
        data["status"] = status
        data["update_time"] = getTime()
        taskSta = TaskPrivateText.query.filter_by(guid=self.guid, user_id=self.user_id).update(data)
        if taskSta is not None:
            db.session.commit()
            return True
        return False

    def byListPage(self):
        db.session.commit()
        u = TaskPrivateText.query.filter_by(status=self.status).order_by(TaskPrivateText.id.desc()).paginate(page=self.iPage,
                                                                                                     per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList


    def byGuidDetails(self):
        db.session.commit()
        d = TaskPrivateText.query.filter_by(guid=self.guid).first()
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


    def byTaskIdDetails(self):
        db.session.commit()
        d = TaskPrivateText.query.filter_by(task_id=self.task_id).first()
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
        list = TaskPrivateText.query.filter_by(status=1).all()
        if len(list) >= 1:
            dictList = dictToListJoinDict(list)
            return dictList
        return False


    def byGuidDel(self):
        stu = TaskPrivateText.query.filter(TaskPrivateText.task_id == self.task_id).delete()
        stuDel = db.session.commit()
        print(stu)
        print(stuDel)