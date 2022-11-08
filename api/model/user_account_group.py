# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from model.user_account_group_user import UserAccountGroupUser


class UserAccountGroup(db.Model):
    __tablename__ = 'tg_user_account_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), unique=False, index=True)
    user_account_id = db.Column(db.String(38), unique=False, index=True)
    channel_id = db.Column(db.String(200))
    channel_title = db.Column(db.String(600))
    channel_username = db.Column(db.String)
    channel_access_hash = db.Column(db.String)
    avatar = db.Column(db.String)
    group_info = db.Column(db.String)
    # 是否需要验证加群:1/验证,2/不验证,3/第三方验证
    approval = db.Column(db.Integer)
    # 加群人数
    group_size = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)

    iPage = 1

    def __init__(self, guid=None, user_id=None, user_account_id=None,
                 channel_id=None,
                 channel_title=None,
                 channel_username=None,
                 channel_access_hash=None,
                 avatar=None,
                 group_info=None, approval=None, group_size=None, is_group=1, status=1, page=1):
        self.guid = guid
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.channel_username = channel_username
        self.channel_access_hash = channel_access_hash
        self.group_info = group_info
        self.approval = approval
        self.group_size = group_size
        self.avatar = avatar
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
        data["channel_title"] = self.channel_title
        data["channel_username"] = self.channel_username
        data["channel_access_hash"] = self.channel_access_hash
        data["update_time"] = getTime()
        user = UserAccountGroup.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = UserAccountGroup.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def byList(self):
        db.session.commit()
        ilist = []
        if self.user_account_id:
            ilist = UserAccountGroup.query.filter_by(status=self.status, user_account_id=self.user_account_id).all()
        else:
            ilist = UserAccountGroup.query.filter_by(status=self.status).all()
        items = dictToListJoinDict(ilist)
        return items

    def byUserAccountIdList(self, user_account_id=None):
        db.session.commit()
        ilist = []
        if user_account_id:
            ilist = UserAccountGroup.query.filter_by(user_account_id=user_account_id).all()
            items = dictToListJoinDict(ilist)
            return items
        return ilist

    def byUserIdList(self, user_id=None):
        db.session.commit()
        ilist = []
        if user_id:
            ilist = UserAccountGroup.query.filter_by(user_id=user_id).all()
            items = dictToListJoinDict(ilist)
            return items
        return ilist

    def byUserAccountIdCount(self):
        db.session.commit()
        count = UserAccountGroup.query.filter_by(user_account_id=self.user_account_id).count()
        if count:
            return count
        return 0

    def byGuidDetails(self):
        db.session.commit()
        d = UserAccountGroup.query.filter_by(guid=self.guid).first()
        detail = {}
        if d:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["user_id"] = d.user_id
            detail["user_account_id"] = d.user_account_id
            detail["channel_id"] = d.channel_id
            detail["channel_title"] = d.channel_title
            detail["channel_username"] = d.channel_username
            detail["channel_access_hash"] = d.channel_access_hash
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return None

    def byChannelIdDetails(self):
        db.session.commit()
        d = UserAccountGroup.query.filter_by(channel_id=self.channel_id).first()
        # db.session.commit()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["user_id"] = d.user_id
            detail["user_account_id"] = d.user_account_id
            detail["channel_id"] = d.channel_id
            detail["channel_title"] = d.channel_title
            detail["channel_title"] = d.channel_title
            detail["channel_username"] = d.channel_username
            detail["channel_access_hash"] = d.channel_access_hash
            detail["status"] = d.status
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
            return detail
        return False

    def byGuidInList(self, guidList=[]):
        db.session.commit()
        list = UserAccountGroup.query.filter(UserAccountGroup.guid.in_(guidList)).all()
        # db.session.commit()
        mger = []
        if len(list) >= 1:
            for v in list:
                tmp = {
                    "id": v.guid,
                    "channel_id": v.channel_id,
                    "channel_title": v.channel_title,
                    "channel_username": v.channel_username,
                    "channel_access_hash": v.channel_access_hash,
                }
                mger.append(tmp)
        if len(mger) >= 1:
            return mger
        else:
            return None

    def handleSearchName(self, channel_title=None):
        # print(username)
        search = "%{}%".format(channel_title)
        db.session.commit()
        items = UserAccountGroup.query.filter_by(status=1, user_id=self.user_id).filter(
            UserAccountGroup.channel_title.like(search)).all()
        inList = []
        if items:
            for val in items:
                inList.append(val.guid)

        # 查询成员
        uaguList = UserAccountGroupUser.query.filter(UserAccountGroupUser.user_account_group_id.in_(inList)).filter(
            UserAccountGroupUser.tg_username.isnot(None)).all()
        if len(uaguList):
            ilist = []
            for v in uaguList:
                tmp = {}
                if len(v.tg_username) != 0:
                    tmp["user_account_id"] = v.user_account_id
                    tmp["user_account_group_id"] = v.user_account_group_id
                    tmp["tg_username"] = v.tg_username
                    tmp["tg_access_hash"] = v.tg_access_hash
                    tmp["tg_user_id"] = v.tg_user_id
                    tmp["tg_nicename"] = v.tg_nicename
                    tmp["tg_phone"] = v.tg_phone
                    ilist.append(tmp)
                else:
                    print("这是处理空字符串..")
                    print("\n\r\n\r\n\r\n")
            return ilist
        return []
