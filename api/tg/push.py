# coding:utf-8
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import SendMessageRequest, CreateChatRequest
from telethon.errors import UsersTooFewError, UserRestrictedError
from tg.tg import Tg

from tools.logs import log

class Push(Tg):
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

    # 发送私人
    def personal(self):
        result = self.client(SendMessageRequest(self.to, self.msg))
        self.__result = result

    # 发送群
    def group(self):
        result = self.client(SendMessageRequest(PeerChannel(self.to), self.msg))
        self.__result = result

    # 发送频道
    def channel(self):
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
