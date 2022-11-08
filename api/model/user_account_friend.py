# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from tools.passwd import createPasswd
import random


class UserAccountFriend(db.Model):
    __tablename__ = 'tg_user_account_friend'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), unique=False, index=True)
    user_account_id = db.Column(db.String(38), unique=False, index=True)
    account_id = db.Column(db.String)
    account_name = db.Column(db.String)
    key = db.Column(db.String(100), unique=False)
    name = db.Column(db.String(100), unique=False)
    avatar = db.Column(db.String(38), default=0)
    account_name = db.Column(db.String(120), default=0)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)

    iPage = 1

    def __init__(self, guid=None, key=None, user_id=None, user_account_id=None, account_id=None, account_name=None,
                 status=1, name=None, avatar=None, page=1):
        self.guid = guid
        self.key = key
        self.name = name
        self.avatar = avatar
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.account_id = account_id
        self.account_name = account_name
        self.status = status
        self.iPage = page

    def insert(self):
        self.guid = str(getGuid())
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        return db.session.commit()

    def update(self):
        data = {}
        data["account_name"] = self.account_name
        data["name"] = self.name
        data["avatar"] = self.avatar
        data["update_time"] = getTime()
        user = UserAccountFriend.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = UserAccountFriend.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def byListPage(self):
        db.session.commit()
        u = UserAccountFriend.query.filter_by(status=self.status).paginate(page=self.iPage, per_page=10)
        # db.session.commit()
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byGuidDetails(self):
        db.session.commit()
        d = UserAccountFriend.query.filter_by(guid=self.guid).first()
        # db.session.commit()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["user_id"] = d.user_id
            detail["user_account_id"] = d.user_account_id
            detail["account_id"] = d.account_id
            detail["account_name"] = d.account_name
            detail["key"] = d.key
            detail["name"] = d.name
            detail["avatar"] = d.avatar
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None
