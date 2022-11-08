#!/usr/bin/env python
# -*- coding:utf-8 -*-

# from telethon import TelegramClient, sync,events
# import logging
# import random
# import asyncio
# import telethon
# from telethon.tl.types import PeerUser, PeerChat, PeerChannel,UpdateNewChannelMessage
# from telethon.tl.functions.messages import SendMessageRequest
# from telethon.tl import types, functions
from tg.tg import Tg
from telethon import utils
from model.user_account import UserAccount

import time


class Me(Tg):

    def test(self):
        try:
            peer = self.client.get_input_entity('@cfg168')  # 可更换用户名
            peer = utils.get_input_peer(peer)
            print(peer)
        except BaseException as err:
            print(err)


    def isStatusAuto(self, tid=None, rootDir=None):
        ua = UserAccount(guid=tid)
        dat = ua.byGuidDetails()
        if dat != None:
            self.rootDir = rootDir
            self.iname = dat['api_name']
            self.api_id = dat['api_id']
            self.api_hash = dat['api_hash']
            self.iphone = dat['phone']
            self.proof = dat['proof']
            self.init()
            dat = self.client.get_me()
            if dat is None:
                ua.upStatusInvalid()
        return True
