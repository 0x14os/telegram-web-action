# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from telethon.sync import TelegramClient
# from telethon.tl.functions.users import GetFullUserRequest
# from telethon.tl.types import PeerUser, PeerChat, PeerChannel, UpdateNewChannelMessage
# from telethon.tl.functions.messages import SendMessageRequest
# from telethon.tl import types, functions
# from telethon import utils
#
# from tools.help import getTime, toTime

rootDir = os.path.abspath(os.path.dirname(__file__))



class RegACC():
    # android id to keys
    api_id = 4
    api_hash = "014b35b6184100b085b0d0572f9b5103"
    client = None
    phone = None
    pathFile = None
    iphone = None

    def __init__(self, phone=None):
        self.iphone = "+" + phone
        self.phone = phone
        # print(self.seeFile)
        # print(self.iphone)

    def __getHashAndCode(self, rootDir=None):
        autoFile = "/auto/" + self.phone
        self.pathFile = rootDir + autoFile
        print(self.pathFile)
        self.client = TelegramClient(self.pathFile, self.api_id, self.api_hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.iphone)
            phone_code_hash = self.client.send_code_request(self.iphone).phone_code_hash
            if phone_code_hash is not None:
                return phone_code_hash
        return None

    def reg(self, code=None):
        phone_code_hash = self.__getHashAndCode()
        # 接码
        client = TelegramClient(self.seefile, self.api_id, self.api_hash)
        client.connect()
        client.sign_in(phone=self.iphone, code=code, phone_code_hash=phone_code_hash)
        if client.get_me() is not None:
            return True
        else:
            return False

    def getHashCode(self, rootDir=None):
        return self.__getHashAndCode(rootDir=rootDir)

    def byHashCodeReg(self, hashCode=None, code=None):
        print(print(self.pathFile))
        # 接码
        client = TelegramClient(self.pathFile, self.api_id, self.api_hash)
        client.connect()
        client.sign_in(phone=self.iphone, code=code, phone_code_hash=hashCode)
        if client.get_me() is not None:
            return True
        else:
            return False


if __name__ == '__main__':
    try:
        # 获取号码组
        # 随机号码
        # 注入号码注册，获取短信code
        regacc = RegACC(phone="111111")
        print(regacc.getHashCode(rootDir=rootDir))
        # print(regacc.byHashCodeReg())
        # 注入code，获取id
        # print(regacc.reg(code=12333))
    except BaseException as err:
        print(err)