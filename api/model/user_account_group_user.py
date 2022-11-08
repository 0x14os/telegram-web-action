# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getTime, setPageing, dictToListJoinDict, getGuid


class UserAccountGroupUser(db.Model):
    __tablename__ = 'tg_user_account_group_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), unique=False, index=True)
    user_account_id = db.Column(db.String(38), unique=False, index=True)
    user_account_group_id = db.Column(db.String(38), unique=False, index=True)
    channel_id = db.Column(db.String(200))
    channel_title = db.Column(db.String(500))
    channel_username = db.Column(db.String)
    # channel_access_hash = db.Column(db.String)
    tg_username = db.Column(db.String)
    tg_user_id = db.Column(db.String)
    tg_access_hash = db.Column(db.String)
    tg_nicename = db.Column(db.String)
    tg_phone = db.Column(db.String)
    tg_last_time = db.Column(db.String(200))
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)


    addAll = None

    iPage = 1

    def __init__(self, guid=None,
                 user_id=None,
                 user_account_id=None,
                 channel_id=None,
                 channel_title=None,
                 channel_username=None,
                 # channel_access_hash=None,
                 user_account_group_id=None,
                 tg_user_id=None,
                 tg_username=None,
                 tg_access_hash=None,
                 tg_nicename=None,
                 tg_phone=None,
                 tg_last_time=None,
                 status=1, page=1):
        self.guid = guid
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.channel_username = channel_username
        # self.channel_access_hash = channel_access_hash
        self.user_account_group_id = user_account_group_id
        self.tg_user_id = tg_user_id
        self.tg_username = tg_username
        self.tg_access_hash = tg_access_hash
        self.tg_nicename = tg_nicename
        self.tg_phone = tg_phone
        self.tg_last_time = tg_last_time

        self.status = status
        self.iPage = page

    def insertAll(self):
        db.session.add_all(self.addAll)
        return db.session.commit()

    def insert(self):
        self.guid = str(getGuid())
        self.status = 1
        self.create_time = getTime()
        self.update_time = getTime()
        # print(self)
        db.session.add(self)
        return db.session.commit()

    def update(self):
        data = {}
        data["update_time"] = getTime()
        user = UserAccountGroupUser.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def isGroupUser(self):
        db.session.commit()
        detail = UserAccountGroupUser.query.filter_by(channel_id=self.channel_id, tg_user_id=self.tg_user_id).first()
        if detail == None:
            return True
        else:
            return False

    def delete(self):
        msg = UserAccountGroupUser.query.filter_by(guid=self.task_id).delete()
        if msg is not None:
            db.session.delete(msg)
            return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = UserAccountGroupUser.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def byListPage(self):
        db.session.commit()
        u = UserAccountGroupUser.query.filter_by(status=1, user_account_group_id=self.user_account_group_id).order_by(
            UserAccountGroupUser.create_time.desc()).paginate(
            page=self.iPage, per_page=20)
        # db.session.commit()
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byUserAllPage(self):
        db.session.commit()
        u = UserAccountGroupUser.query.filter_by(status=1, user_id=self.user_id).order_by(
            UserAccountGroupUser.create_time.desc()).paginate(
            page=self.iPage, per_page=30)
        # db.session.commit()
        items = dictToListJoinDict(u.items)
        u.items = items
        pageList = setPageing(u)
        return pageList

    def byUserIdList(self):
        db.session.commit()
        list = UserAccountGroupUser.query.filter_by(status=1, user_id=self.user_id).order_by(
            UserAccountGroupUser.create_time.desc()).all()
        # db.session.commit()
        items = []
        if list:
            items = dictToListJoinDict(list)
        return items

    def byUserTIdList(self):
        db.session.commit()
        list = UserAccountGroupUser.query.filter_by(status=1,
                                                    user_account_id=self.user_account_id).order_by(
            UserAccountGroupUser.create_time.desc()).all()
        # db.session.commit()
        items = []
        if list:
            items = dictToListJoinDict(list)
        return items

    # 检查需要导入的用户，编排数据结构类型，便于查找实体类
    def checkByUserIdTgUserName(self):
        ilist = self.byUserIdList()
        tlist = []
        if len(ilist) > 0:
            for v in ilist:
                tmp = {}
                tmp["id"] = v['tg_user_id']
                tmp["access_hash"] = v['tg_access_hash']
                tmp["username"] = v['tg_username']
                tmp["nicename"] = v['tg_nicename']
                tmp["tg_last_time"] = v['tg_last_time']
                if v['tg_username']:
                    tmp["type"] = 1
                else:
                    tmp["type"] = 2
                tlist.append(tmp)
        return tlist
