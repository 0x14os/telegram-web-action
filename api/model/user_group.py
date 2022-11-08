# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from tools.passwd import createPasswd
import random


class UserGroup(db.Model):
    __tablename__ = 'tg_user_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    moduleId = db.Column(db.String(38), default=38)
    name = db.Column(db.String(100), unique=False)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)

    iPage = 1

    def __init__(self, guid=None, moduleId=None, name=None, status=1, page=1):
        self.guid = guid
        self.moduleId = moduleId
        self.name = name
        self.status = status
        self.iPage = page

    def insert(self):
        self.guid = str(getGuid())
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        if db.session.commit():
            return True
        else:
            return False

    def update(self):
        data = {}
        if self.name != None:
            data["name"] = self.name

        if self.moduleId != None:
            data["moduleId"] = self.moduleId
        data["update_time"] = getTime()
        user = UserGroup.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            db.session.commit()
            return True
        return False

    def delete(self):
        user = UserGroup.query.filter_by(guid=self.guid).first()
        if user != None:
            db.session.delete(user)
            return db.session.commit()
        return False

    def byListPage(self):
        db.session.commit()
        list = UserGroup.query.filter_by(status=self.status).paginate(page=self.iPage, per_page=10)
        items = dictToListJoinDict(list.items)
        list.items = items
        pageList = setPageing(list)
        return pageList

    def byGuidDetails(self):
        db.session.commit()
        d = UserGroup.query.filter_by(guid=self.guid).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["name"] = d.name
            detail["moduleId"] = d.moduleId
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None
