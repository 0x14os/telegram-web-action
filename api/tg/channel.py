#!/usr/bin/env python
# -*- coding:utf-8 -*-

from telethon.tl.functions.channels import JoinChannelRequest

from tg.tg import Tg

import time

class Channel(Tg):

    def test(self):
        # myself = self.client.get_me()
        # print(myself)
        result = self.client(JoinChannelRequest(channel="https://t.me/yifeng666"))
        print(result.stringify())

    def joinGroup(self, usernName=None):
        if usernName != None:
            try:
                self.client(JoinChannelRequest(channel=usernName))
                # print(result.stringify())
                # print(result)
            except BaseException as err:
                print(err)

    def joinNGroup(self, usernName=None):
        if usernName != None or len(usernName) > 0:
            try:
                for v in usernName:
                    # print(v)
                    if v != None:
                        self.client(JoinChannelRequest(channel=v))
                    time.sleep(2)
            except BaseException as err:
                print("joinNGroup:",err)
