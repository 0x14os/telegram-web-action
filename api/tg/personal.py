# coding:utf-8
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import SendMessageRequest, CreateChatRequest
from telethon.errors import UsersTooFewError, UserRestrictedError
from tg.tg import Tg

from tools.logs import log


class Personal(Tg):
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

    # 推送消息
    def pushMsg(self):
        result = self.client(SendMessageRequest(self.to, self.msg))
        self.__result = result

    # 返回结果
    def result(self):
        return self.__result
