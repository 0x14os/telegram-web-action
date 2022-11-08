# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime,dictToListJoinDict, toDate



class Msg(db.Model):
    __tablename__ = 'tg_msg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38))
    user_id = db.Column(db.String(38))
    title = db.Column(db.String(80))
    content = db.Column(db.String)
    status = db.Column(db.Integer, default=1)
    type = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=10)
    update_time = db.Column(db.Integer, default=10)

    iPage = 1

    def __init__(self, guid=None, user_id=None, title=None, text=None,
                 status=1, page=1):
        self.guid = guid
        self.user_id = user_id
        self.title = title
        self.content = text
        self.status = status
        self.iPage = page

    def insert(self):
        self.guid = str(getGuid())
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        return db.session.commit()

    def upStatus(self):
        data = {}
        data["update_time"] = getTime()
        data["status"] = 2
        user = Msg.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                db.session.commit()
                return True
        return False

    def delete(self):
        msg = Msg.query.filter_by(guid=self.guid).delete()
        if msg is not None:
            db.session.commit()
            return True
        return False

    def byUserIdList(self):
        db.session.commit()
        list = Msg.query.filter_by(user_id=self.user_id).order_by(Msg.id.desc()).all()
        if list:
            items = dictToListJoinDict(list)
            return items
        return None

    def byUserIdOne(self):
        db.session.commit()
        d = Msg.query.filter_by(user_id=self.user_id).filter_by(status=1).order_by(Msg.id.desc()).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["title"] = d.title
            detail["content"] = d.content
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None

    # 根据用户id查询有任務
    def byUserIdCount(self):
        db.session.commit()
        count = Msg.query.filter_by(user_id=self.user_id).filter_by(status=1).count()
        if count:
            return count
        return 0
