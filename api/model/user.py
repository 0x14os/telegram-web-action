# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from tools.passwd import createPasswd
import random


class User(db.Model):
    __tablename__ = 'tg_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    email = db.Column(db.String(38), unique=False)
    password = db.Column(db.String(360), unique=False)
    password_random = db.Column(db.String(20), default=0)
    token = db.Column(db.String(360), default=0)
    role_use = db.Column(db.Integer, default=2)
    last_ip = db.Column(db.String(210), default=0)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=0)
    login_count = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)
    groupId = db.Column(db.String(38), default=38)
    taskNumber = db.Column(db.Integer, default=0)
    tgNumber = db.Column(db.Integer, default=0)
    tgGroupNumber = db.Column(db.Integer, default=0)

    iPage = 1

    def __init__(self, guid=None, email=None, password=None, token=None, last_ip=None, login_count=1, status=1,
                 groupId='', tgNumber=0,taskNumber=0, tgGroupNumber=0, page=1):
        self.guid = guid
        self.email = email
        self.password = password
        self.token = token
        self.last_ip = last_ip
        self.login_count = login_count
        self.groupId = groupId
        self.taskNumber = taskNumber
        self.tgNumber = tgNumber
        self.tgGroupNumber = tgGroupNumber
        self.status = status
        self.iPage = page

    def insert(self):
        password_random = random.randrange(0, 101, 8)
        pwd = self.password + str(password_random)
        passwd = createPasswd(pwd)
        self.guid = str(getGuid())
        self.password = passwd
        self.password_random = password_random
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        db.session.add(self)
        return db.session.commit()

    def upLoginToken(self):
        data = {}
        data["token"] = self.token
        data["last_ip"] = self.last_ip
        data["login_count"] = self.login_count
        data["update_time"] = getTime()
        user = User.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def update(self):
        data = {}

        if self.taskNumber != 0:
            data["taskNumber"] = self.taskNumber

        if self.tgNumber != 0:
            data["tgNumber"] = self.tgNumber

        if self.tgGroupNumber != 0:
            data["tgGroupNumber"] = self.tgGroupNumber
        data["update_time"] = getTime()
        user = User.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.password != None:
                return db.session.commit()
        return False

    def updatePasswd(self):
        password_random = random.randrange(0, 101, 8)
        pwd = self.password + str(password_random)
        passwd = createPasswd(pwd)
        data = {}
        data["password"] = passwd
        data["password_random"] = password_random
        data["update_time"] = getTime()
        user = User.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            return db.session.commit()
        return False

    def delete(self):
        user = User.query.filter_by(guid=self.guid).first()
        if user != None:
            db.session.delete(user)
            return db.session.commit()
        return False

    def byListPage(self):
        db.session.commit()
        u = User.query.filter_by(status=self.status).paginate(page=self.iPage, per_page=10)
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byEmailDetails(self):
        db.session.commit()
        d = User.query.filter_by(email=self.email).first()
        # db.session.commit()
        detail = {}
        if d:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["email"] = d.email
            detail["password"] = d.password
            detail["password_random"] = d.password_random
            detail["token"] = d.token
            detail["role_use"] = d.role_use
            detail["last_ip"] = d.last_ip
            detail["login_count"] = d.login_count
            detail["taskNumber"] = d.taskNumber
            detail["tgNumber"] = d.tgNumber
            detail["tgGroupNumber"] = d.tgGroupNumber
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return False

    def byGuidDetails(self):
        db.session.commit()
        d = User.query.filter_by(guid=self.guid).first()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["email"] = d.email
            detail["password"] = d.password
            detail["password_random"] = d.password_random
            detail["token"] = d.token
            detail["role_use"] = d.role_use
            detail["last_ip"] = d.last_ip
            detail["login_count"] = d.login_count
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None
