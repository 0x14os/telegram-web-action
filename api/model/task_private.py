# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate


class TaskPrivate(db.Model):
    __tablename__ = 'tg_task_private'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), unique=False, index=True)
    userAccountIdList = db.Column(db.Text)
    sendNumber = db.Column(db.Integer, default=10)
    sendAccountNumber = db.Column(db.Integer, default=10)
    accountNumber = db.Column(db.Integer, default=10)
    title = db.Column(db.String(120))
    soKey = db.Column(db.String(300))
    remark = db.Column(db.String(30))
    # 休眠时间
    timer = db.Column(db.Integer, default=5)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)

    iPage = 1

    def __init__(self, guid=None, user_id=None, userAccountIdList=None, sendNumber=0, accountNumber=0,
                 sendAccountNumber=0,
                 title=None, soKey=None, remark=None, timer=0, status=1,
                 page=1):
        self.guid = guid
        self.user_id = user_id
        self.userAccountIdList = userAccountIdList
        self.sendNumber = sendNumber
        self.accountNumber = accountNumber
        self.sendAccountNumber = sendAccountNumber
        self.soKey = soKey
        self.remark = remark
        self.timer = timer
        self.title = title
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
        data["userAccountIdList"] = self.userAccountIdList
        data["sendNumber"] = self.sendNumber
        data["sendAccountNumber"] = self.sendAccountNumber
        data["title"] = self.title
        data["soKey"] = self.soKey
        data["remark"] = self.remark
        # 休眠时间
        data["timer"] = self.timer
        data["update_time"] = getTime()
        user = TaskPrivate.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def edit(self):
        data = {}
        data["title"] = self.title
        data["remark"] = self.remark
        # 休眠时间
        data["timer"] = self.timer
        data["update_time"] = getTime()
        user = TaskPrivate.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def updateSendNumber(self):
        data = {}
        data["sendNumber"] = self.sendNumber
        data["update_time"] = getTime()
        user = TaskPrivate.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = TaskPrivate.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # 删除
    def byGuidInUidDel(self, status=2):
        data = {}
        data["status"] = status
        data["update_time"] = getTime()
        taskSta = TaskPrivate.query.filter_by(guid=self.guid, user_id=self.user_id).update(data)
        if taskSta is not None:
            db.session.commit()
            return True
        return False

    def byListPage(self):
        db.session.commit()
        u = TaskPrivate.query.filter_by(user_id=self.user_id).order_by(TaskPrivate.id.desc()).paginate(page=self.iPage,
                                                                                                       per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byUidListPage(self):
        db.session.commit()
        u = TaskPrivate.query.filter_by(status=self.status).filter_by(user_id=self.user_id).order_by(
            TaskPrivate.id.desc()).paginate(
            page=self.iPage, per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byGuidDetails(self):
        db.session.commit()
        d = TaskPrivate.query.filter_by(guid=self.guid).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["user_id"] = d.user_id
            detail["userAccountIdList"] = d.userAccountIdList
            detail["sendAccountNumber"] = d.sendAccountNumber
            detail["accountNumber"] = d.accountNumber
            detail["sendNumber"] = d.sendNumber
            detail["title"] = d.title
            detail["soKey"] = d.soKey
            detail["remark"] = d.remark
            detail["timer"] = d.timer
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None

    def getTaskApsList(self):
        db.session.commit()
        list = TaskPrivate.query.filter_by(status=1).all()
        if len(list) >= 1:
            dictList = dictToListJoinDict(list)
            return dictList
        return False

    # 根据用户id查询有任務
    def byUserIdTaskCount(self):
        db.session.commit()
        count = TaskPrivate.query.filter_by(user_id=self.user_id).filter_by(status=1).count()
        if count:
            return count
        return 0

    def byGuidDel(self):
        TaskPrivate.query.filter(TaskPrivate.guid == self.guid).delete()
        db.session.commit()
        return True

    def stop(self):
        data = {}
        data["status"] = 1
        data["update_time"] = getTime()
        TaskPrivate.query.filter_by(guid=self.guid).update(data)
        db.session.commit()
        return True

    def start(self):
        data = {}
        data["status"] = 2
        data["update_time"] = getTime()
        TaskPrivate.query.filter_by(guid=self.guid).update(data)
        db.session.commit()
        return True

    def finish(self):
        data = {}
        data["status"] = 3
        data["update_time"] = getTime()
        TaskPrivate.query.filter_by(guid=self.guid).update(data)
        db.session.commit()
        return True
