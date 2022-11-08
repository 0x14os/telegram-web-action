# !/usr/bin/env python
# -*- coding:utf-8 -*-
from model.dbconf import db
from tools.help import getGuid, getTime, setPageing, dictToListJoinDict, toDate
from model.user_account_group import UserAccountGroup
from model.task import Task


class UserAccount(db.Model):
    __tablename__ = 'tg_user_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(38), unique=True, index=True)
    user_id = db.Column(db.String(38), index=True)
    api_id = db.Column(db.String(100), unique=False)
    api_name = db.Column(db.String(100), unique=False)
    api_hash = db.Column(db.String(100), unique=False)
    api_certificate = db.Column(db.Text)

    username = db.Column(db.String(120), default=0)
    phone = db.Column(db.String(50), default=0)
    phone_code_hash = db.Column(db.String(255), default=0)

    is_activation = db.Column(db.Integer, default=1)
    is_group = db.Column(db.Integer, default=1)

    is_new_group = db.Column(db.Integer, default=1)
    new_group_list = db.Column(db.Text)
    # 凭证
    proof = db.Column(db.Text)
    new_group_name = db.Column(db.String(255), default=0)

    status = db.Column(db.Integer, default=1)
    mode = db.Column(db.Integer, default=1)
    create_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)

    iPage = 1

    def __init__(self, guid=None,
                 user_id=None,
                 api_id=None,
                 api_name=None,
                 api_hash=None,
                 api_certificate=None,
                 username=None,
                 proof=None,
                 is_new_group=1,
                 new_group_list=None,
                 new_group_name=None,
                 is_activation=1,
                 phone=None, status=1, is_group=1, mode=1,
                 page=1):
        self.guid = guid
        self.user_id = user_id
        self.api_id = api_id
        self.api_name = api_name
        self.api_hash = api_hash
        self.api_certificate = api_certificate
        self.username = username
        self.proof = proof
        self.phone = phone
        self.is_group = is_group

        self.is_activation = is_activation
        self.is_new_group = is_new_group
        self.new_group_list = new_group_list
        self.new_group_name = new_group_name

        self.mode = mode
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
        data["username"] = self.username
        data["phone"] = self.phone
        data["api_id"] = self.api_id
        data["api_hash"] = self.api_hash
        data["api_name"] = self.api_name
        data["api_certificate"] = self.api_certificate
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upPhoneHash(self, code_hash=None, proof=None):
        data = {}
        data["phone_code_hash"] = code_hash
        data["proof"] = proof
        data["is_activation"] = 1
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # 新建群
    def upNewGroup(self, is_new_group=2):
        data = {}
        data["is_new_group"] = is_new_group
        data["new_group_list"] = self.new_group_list
        data["new_group_name"] = self.new_group_name
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                db.session.commit()
                return True
        return False

    # 清空群缓存
    def upNewGroupDelCahce(self):
        data = {}
        data["is_new_group"] = 1
        data["new_group_list"] = ""
        data["new_group_name"] = ""
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                db.session.commit()
                return True
        return False

    def upGroupStatus(self):
        data = {}
        data["is_group"] = self.is_group
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upActivation(self):
        data = {}
        data["is_activation"] = 2
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    def upStatus(self):
        data = {}
        data["status"] = self.status
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # id Invalid
    def upStatusInvalid(self):
        data = {}
        data["status"] = 2
        data["is_activation"] = 3
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=self.guid).update(data)
        if user is not None:
            if self.guid != None:
                return db.session.commit()
        return False

    # id Invalid
    def byUpTidStatusInvalid(self, tid=None):
        data = {}
        data["status"] = 2
        data["is_activation"] = 3
        data["update_time"] = getTime()
        user = UserAccount.query.filter_by(guid=tid).update(data)
        if user is not None:
            return db.session.commit()
        return False

    # 根据用户id查询有多少账号
    def byUserIdTgCount(self):
        db.session.commit()
        count = UserAccount.query.filter_by(user_id=self.user_id).filter_by(status=1).count()
        if count:
            return count
        return 0

    def byListPage(self):
        db.session.commit()
        u = UserAccount.query.filter_by(user_id=self.user_id).order_by(
            UserAccount.create_time.desc()).paginate(page=self.iPage, per_page=30)
        items = dictToListJoinDict(u.items)
        listTmp = []
        if type(items) == list:
            for dictVal in items:
                dictVal["group_count"] = 0
                dictVal["task_count"] = 0
                uagCount = UserAccountGroup(user_account_id=dictVal["guid"])
                igcount = uagCount.byUserAccountIdCount()

                if igcount != 0:
                    dictVal["group_count"] = igcount

                itaskCount = Task(user_account_id=dictVal["guid"])
                itCount = itaskCount.byUserAccountIdCount()
                if itCount != 0:
                    dictVal["task_count"] = itCount
                listTmp.append(dictVal)

        u.items = listTmp
        pageList = setPageing(u)
        return pageList

    def byStatusListPage(self, is_activation=None):
        db.session.commit()
        u = UserAccount.query.filter_by(user_id=self.user_id).filter_by(is_activation=is_activation).order_by(
            UserAccount.create_time.desc()).paginate(page=self.iPage, per_page=30)
        items = dictToListJoinDict(u.items)
        listTmp = []
        if type(items) == list:
            for dictVal in items:
                dictVal["group_count"] = 0
                dictVal["task_count"] = 0
                uagCount = UserAccountGroup(user_account_id=dictVal["guid"])
                igcount = uagCount.byUserAccountIdCount()

                if igcount != 0:
                    dictVal["group_count"] = igcount

                itaskCount = Task(user_account_id=dictVal["guid"])
                itCount = itaskCount.byUserAccountIdCount()
                if itCount != 0:
                    dictVal["task_count"] = itCount
                listTmp.append(dictVal)

        u.items = listTmp
        pageList = setPageing(u)
        return pageList

    def handleSearchName(self, username=None):
        # print(username)
        search = "%{}%".format(username)
        db.session.commit()
        items = UserAccount.query.filter_by(status=1, user_id=self.user_id).filter(
            UserAccount.username.like(search)).all()
        items = dictToListJoinDict(items)
        list = []
        if items:
            for val in items:
                tmp = {}
                tmp['tid'] = val['guid']
                tmp['username'] = val['username']
                list.append(tmp)
        return list

    def byUserIdList(self, userId=None):
        db.session.commit()
        items = UserAccount.query.filter_by(status=1, mode=1, user_id=userId).all()
        items = dictToListJoinDict(items)
        list = []
        if items:
            for val in items:
                tmp = {}
                # TG账号guid简称
                tmp['tid'] = val['guid']
                tmp['username'] = val['username']
                list.append(tmp)
        return list

    def byGuidDetails(self):
        db.session.commit()
        d = UserAccount.query.filter_by(guid=self.guid).first()
        # db.session.commit()
        detail = {}
        if d != None:
            detail["id"] = d.id
            detail["guid"] = d.guid
            detail["user_id"] = d.user_id
            detail["proof"] = d.proof
            detail["api_id"] = d.api_id  # str(d.api_id,encoding='utf-8')
            detail["api_hash"] = d.api_hash
            detail["api_name"] = d.api_name
            detail["api_certificate"] = d.api_certificate
            detail["phone"] = d.phone
            detail["username"] = d.username
            detail["phone_code_hash"] = d.phone_code_hash
            detail["status"] = d.status  # str(d.status,encoding='utf-8')
            detail["is_activation"] = d.is_activation  # str(d.is_activation,encoding='utf-8')
            # d.is_activation
            detail["is_group"] = d.is_group  # str(d.is_group,encoding='utf-8')
            # d.is_group
            detail["is_new_group"] = d.is_new_group  # str(d.is_new_group, encoding='utf-8')
            # d.is_new_group
            detail["new_group_list"] = d.new_group_list
            detail["new_group_name"] = d.new_group_name
            detail["mode"] = d.mode
            detail["create_time"] = toDate(d.create_time)
            detail["update_time"] = toDate(d.update_time)
        return detail

    def joinUser(self):
        db.session.commit()
        query = db.session.query(UserAccount, Task).filter(Task.user_account_id == UserAccount.guid).filter(
            Task.status == 1).all()
        # db.session.commit()
        tmp = []
        if len(query) >= 1:
            for val in query:
                imap = {}
                imap["user_account_id"] = val.UserAccount.guid
                imap["mode"] = val.UserAccount.mode
                imap["is_activation"] = val.UserAccount.is_activation
                imap["api_id"] = val.UserAccount.api_id
                imap["api_hash"] = val.UserAccount.api_hash
                imap["api_name"] = val.UserAccount.api_name
                imap["api_certificate"] = val.UserAccount.api_certificate
                imap["phone_code_hash"] = val.UserAccount.phone_code_hash
                imap["phone"] = val.UserAccount.phone
                imap["username"] = val.UserAccount.username
                imap["account_status"] = val.UserAccount.status
                imap["task_guid"] = val.Task.guid
                imap["method"] = val.Task.method
                imap["user_id"] = val.Task.user_id
                imap["user_account_group_list"] = val.Task.user_account_group_list
                imap["title"] = val.Task.title
                imap["msg"] = val.Task.msg
                imap["timer"] = val.Task.timer
                imap["remark"] = val.Task.remark
                imap["task_status"] = val.Task.status
                tmp.append(imap)
        return tmp

    # 获取私信账号列表
    def getPrivateSendList(self, limit=0):
        db.session.commit()
        list = UserAccount.query.filter_by(user_id=self.user_id, mode=2, status=1).order_by(
            UserAccount.id.desc()).limit(
            limit).all()
        return list

    def byUserIdAutoList(self, userId=None):
        db.session.commit()
        items = UserAccount.query.filter_by(status=1, is_activation=2, user_id=userId).all()
        if items is not None:
            items = dictToListJoinDict(items)
            return items
        return []
