#!/usr/env/python python
# _*_ coding: utf-8 _*_
from telethon.sync import TelegramClient
from model.user_account import UserAccount

from tools.logs import log


class Tg():
    rootDir = None
    api_id = None
    api_hash = None
    iname = None
    iphone = None
    client = None
    proof = None

    def init(self):
        self.connection()

    def connection(self):
        # print(self.iname, self.api_id, self.api_hash)
        # sessionPath = "/session/" + self.iname
        # print(self.rootDir + self.proof)
        try:
            self.client = TelegramClient(self.rootDir + self.proof, self.api_id, self.api_hash)
            self.client.connect()
        except BaseException as err:
            print(err)

    def getClient(self):
        return self.client

    # 发送验证码
    def webLoginPushCode(self, tid=None):
        # print("push code")
        sessionPath = "/session/" + self.iname
        proof = sessionPath
        self.client = TelegramClient(self.rootDir + sessionPath, self.api_id, self.api_hash)
        try:
            self.client.connect()
        except OSError:
            print('Failed to connect')

        ps = self.client.send_code_request(self.iphone)
        print("ps:", ps)

        if ps.phone_code_hash:
            # code sql
            ua = UserAccount(guid=tid)
            ua.upPhoneHash(code_hash=ps.phone_code_hash, proof=proof)
            return True
        else:
            log.warning("发送失败Tid:%s" % tid)
            return False
        # return False

    # 登陆验证
    def cmdLogin(self, code=None, tid=None, phash=None):
        self.client = TelegramClient(self.rootDir + self.proof, self.api_id, self.api_hash)
        try:
            self.client.connect()
        except OSError:
            print('Failed to connect')
        sign = self.client.sign_in(self.iphone, code=code, phone_code_hash=phash)
        print(sign)
        ua = UserAccount(guid=tid)
        ua.upActivation()