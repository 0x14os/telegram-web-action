# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate


class Task(db.Model):
    __tablename__ = 'tg_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, default=1)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), unique=False, index=True)
    user_account_id = db.Column(db.String(38), unique=False, index=True)
    user_account_group_list = db.Column(db.Text, unique=False)
    send_group_number = db.Column(db.Integer, default=10)
    title = db.Column(db.String(120))
    msg = db.Column(db.Text)
    method = db.Column(db.String(30))
    remark = db.Column(db.String(30))
    timer = db.Column(db.String(30))
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)

    iPage = 1

    def __init__(self, guid=None, user_id=None, user_account_id=None, user_account_group_list=None,
                 send_group_number=None, title=None, msg=None, remark=None, timer=0, method=None, status=1,
                 page=1):
        self.guid = guid
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.user_account_group_list = user_account_group_list
        self.send_group_number = send_group_number
        self.msg = msg
        self.remark = remark
        self.timer = timer
        self.title = title
        self.method = method
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
        data["user_account_group_list"] = self.user_account_group_list
        data["send_group_number"] = self.send_group_number
        data["title"] = self.title
        data["msg"] = self.msg
        data["remark"] = self.remark
        data["timer"] = self.timer
        data["update_time"] = getTime()
        user = Task.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = Task.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def start(self):
        data = {}
        data["status"] = 2
        data["update_time"] = getTime()
        user = Task.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def stop(self):
        data = {}
        data["status"] = 1
        data["update_time"] = getTime()
        user = Task.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # 删除
    def byGuidInUidDel(self, status=2):
        data = {}
        data["status"] = status
        data["update_time"] = getTime()
        taskSta = Task.query.filter_by(guid=self.guid, user_id=self.user_id).update(data)
        # print("status:{}".format(taskSta))
        if taskSta is not None:
            db.session.commit()
            return True
        return False

    def byGuidDel(self):
        Task.query.filter(Task.guid == self.guid).delete()
        db.session.commit()
        return True

    def byListPage(self):
        db.session.commit()
        u = Task.query.filter_by(status=self.status).order_by(Task.id.desc()).paginate(page=self.iPage, per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byUidListPage(self):
        db.session.commit()
        u = Task.query.filter_by(user_id=self.user_id).order_by(Task.id.desc()).paginate(
            page=self.iPage, per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byGuidDetails(self):
        db.session.commit()
        d = Task.query.filter_by(guid=self.guid).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["type"] = d.type
            detail["user_id"] = d.user_id
            detail["user_account_id"] = d.user_account_id
            detail["user_account_group_list"] = d.user_account_group_list
            detail["send_group_number"] = d.send_group_number
            detail["title"] = d.title
            detail["msg"] = d.msg
            detail["remark"] = d.remark
            detail["timer"] = d.timer
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None

    def byUserAccountIdCount(self):
        db.session.commit()
        count = Task.query.filter_by(user_account_id=self.user_account_id).count()
        if count:
            return count
        return 0

    def getTaskApsList(self):
        db.session.commit()
        list = Task.query.filter_by(status=1).all()
        if len(list) >= 1:
            dictList = dictToListJoinDict(list)
            return dictList
        return False

    # 根据用户id查询有任務
    def byUserIdTaskCount(self):
        db.session.commit()
        count = Task.query.filter_by(user_id=self.user_id).filter_by(status=1).count()
        if count:
            return count
        return 0
