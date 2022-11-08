#!/usr/bin/env python
# -*- coding:utf-8 -*-

from telethon.tl.types import PeerChannel, InputPeerEmpty, PeerChat
from telethon.tl.functions.messages import GetDialogsRequest, SendMessageRequest, CreateChatRequest

from telethon.errors import UsersTooFewError, UserRestrictedError

# from telethon.tl.functions.channels import GetParticipantsRequest
# from telethon.tl.types import ChannelParticipantsSearch

from tg.tg import Tg

from model.user_account_group import UserAccountGroup
from model.user_account_group_user import UserAccountGroupUser
from tools.logs import log
from tools.help import toTime
import time
import datetime


# from tools.help import getGuid


class Group(Tg):
    to = None
    msg = None
    __result = None

    userNameList = []
    newName = None

    def __init__(self, to=None, msg=None, newName=None, userNameList=None):
        self.to = to
        self.msg = msg
        self.newName = newName
        self.userNameList = userNameList

    # 获取TG账号列表的所有群信息
    def __getGroupListInfo(self):
        chats = []
        last_date = None
        chunk_size = 5000
        groups = []
        groupList = []
        print("getGroupListInfo")

        result = self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        # print(chats)

        for chat in chats:

            # if chat.default_banned_rights != None:
            #     # print("121212")
            #     groups.append(chat)
            try:
                if chat.megagroup == True:
                    groups.append(chat)
            except:
                continue

        # print(groups)

        for ig in groups:
            tmp = {}
            if ig.id:
                tmp["channel_id"] = ig.id
            if ig.title:
                tmp["channel_title"] = ig.title

            if hasattr(ig, "username"):
                tmp["channel_username"] = ig.username
            else:
                tmp["channel_username"] = "none"

            if hasattr(ig, "access_hash"):
                tmp["channel_access_hash"] = ig.access_hash
            else:
                tmp["channel_access_hash"] = "none"
            groupList.append(tmp)
        return groupList

    # 获取群成员
    def getExtractGroup(self, tgid=None):
        # UserAccountGroupUser
        # print("UserAccountGroupUser")
        uag = UserAccountGroup(guid=tgid)
        details = uag.byGuidDetails()
        # print(details)
        channel_id = int(details['channel_id'])
        # print(channel_id)
        ilist = self.__getGroupUserPage(channel_id=channel_id)
        # print(ilist)
        if ilist or len(ilist):
            for val in ilist:
                self.__addGroupUser(
                    groups=details,
                    tg_username=val['username'],
                    tg_access_hash=val['access_hash'],
                    tg_nicename=val['nicename'],
                    tg_user_id=val['user_id'],
                    tg_phone=val['phone'],
                    tg_last_time=val['tg_last_time'],
                )

    # 设置用户信息
    def __getGroupUserPage(self, channel_id=0):
        userInfo = []
        # 根据群组id获取群组对象
        try:
            entity = PeerChannel(channel_id=int(channel_id))
            channel = self.client.get_entity(entity)
            # print(channel)
            # 获取群组所有用户信息
            responses = self.client.iter_participants(channel, aggressive=True)
            # print(responses)
            for user in responses:
                # print(user)
                userTmp = {}
                if user.first_name is not None:
                    first_name = user.first_name
                else:
                    first_name = ""

                if user.last_name is not None:
                    last_name = user.last_name
                else:
                    last_name = ""

                if user.username is not None:
                    username = user.username
                else:
                    username = ""

                if user.phone is not None:
                    phone = user.phone
                else:
                    phone = ""

                if user.status is not None:
                    # Active within 15 days
                    date = datetime.datetime.now() + datetime.timedelta(days=-15)
                    notDate = date.strftime("%Y-%m-%d %H:%M:%S")
                    notTime = toTime(notDate)
                    # UserStatusRecently is del
                    # UserStatusOffline
                    if type(user.status).__name__ == 'UserStatusOffline':
                        so = user.status
                        if so.was_online is not None:
                            lastDate = so.was_online.strftime("%Y-%m-%d %H:%M:%S")
                            lastTime = toTime(lastDate)
                            if user.bot == False:
                                if lastTime > notTime:
                                    nicename = (first_name + ' ' + last_name).strip()
                                    userTmp["user_id"] = user.id
                                    userTmp["access_hash"] = user.access_hash
                                    userTmp["phone"] = phone
                                    userTmp["username"] = username
                                    userTmp["nicename"] = nicename
                                    userTmp["tg_last_time"] = so.was_online
                                    userInfo.append(userTmp)

        except BaseException as err:
            print("BaseException",err)
        return userInfo

    # 添加群用户
    def __addGroupUser(self, groups=None, tg_username=None, tg_access_hash=None, tg_nicename=None, tg_user_id=None, tg_phone=None,tg_last_time=None):
        # print(groups)
        # print(tg_username, tg_access_hash, tg_nicename, tg_user_id)
        adduser = UserAccountGroupUser(
            user_id=groups['user_id'],
            user_account_id=groups['user_account_id'],
            channel_id=groups['channel_id'],
            channel_title=groups['channel_title'],
            channel_username=groups['channel_username'],
            # channel_access_hash=groups['channel_access_hash'],
            user_account_group_id=groups['guid'],
            tg_username=tg_username,
            tg_access_hash=tg_access_hash,
            tg_nicename=tg_nicename,
            tg_user_id=tg_user_id,
            tg_phone=tg_phone,
            tg_last_time=tg_last_time
        )

        if adduser.isGroupUser():
            adduser.insert()

    # 获取多个群成员列表
    def getGroupListUser(self, groups=[]):
        all_user = []
        numGroup = len(groups)
        for i in range(int(numGroup)):
            i_group = groups[i]
            # 获取成员列表
            groupTmp = self.client.get_participants(i_group, aggressive=True)
            if len(groupTmp) >= 1:
                for user in groupTmp:
                    all_user.append(user)
        return all_user

    # 获取一个群组的成员信息
    def getGroupOneUserInfo(self, groupOne):
        groupTmp = self.client.get_participants(groupOne, aggressive=True)
        return groupTmp

    # 私有处理
    def __setGroupUserInfo(self, objUser):
        return objUser

    # 获取电报群
    def getGroup(self, user_id=None, user_account_id=None):
        list = self.__getGroupListInfo()
        for v in list:
            uag = UserAccountGroup(
                user_id=user_id,
                user_account_id=user_account_id,
                channel_id=v["channel_id"],
                channel_title=v["channel_title"],
                channel_username=v["channel_username"],
                channel_access_hash=v["channel_access_hash"]
            )
            details = uag.byChannelIdDetails()
            if details == False:
                uag.insert()
        print("group number:%d" % len(list))
        return True

    # 推送群消息
    def pushOneMsg(self):
        result = self.client(SendMessageRequest(PeerChannel(self.to), self.msg))
        self.__result = result

    # 发送频道
    def pushChannel(self):
        result = self.client(SendMessageRequest(PeerChannel(self.to), self.msg))
        self.__result = result

    # 新建群
    def newGroup(self):
        try:
            # print([self.newName,self.userNameList])
            result = self.client(CreateChatRequest(self.userNameList, self.newName))
            # print(result.)
        except UsersTooFewError:
            log.error(["UsersTooFewError新建群失败", self.newName, self.userNameList, UsersTooFewError])
            self.__result = False
        except UserRestrictedError:
            log.error(["UserRestrictedError新建群失败", self.newName, self.userNameList, UserRestrictedError])
            self.__result = False
        else:
            self.__result = True


    # 返回结果
    def result(self):
        return self.__result



