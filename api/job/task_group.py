# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from model.user_account import UserAccount
from model.user_account import UserAccountGroup
from job.job_rq import JobRq
from tools.help import md5


class JobTaskGroup:

    def list(self):
        tulist = []
        task = UserAccount()
        # 用户任务列表
        tu = task.joinUser()
        if len(tu) > 0:
            # 声明发送列表
            # print(tu)
            for v in tu:
                # 需要发送的群数量
                group_list = v["user_account_group_list"]
                group_list_guid = group_list.split(",")
                # print(group_list_guid)
                uag = UserAccountGroup()
                # 获取群数据实例
                byGuidInList = uag.byGuidInList(guidList=group_list_guid)
                # print(byGuidInList)
                if byGuidInList:
                    v["group_list"] = byGuidInList
                tulist.append(v)
        return tulist

    def inToList(self):
        jobList = []
        list = self.list()

        if len(list) != 0:
            # 总发送数量
            num = 0
            for val in list:
                jobCmd = {}
                # 发送时间
                date = val["timer"]
                # 当前时间
                toDay = time.strftime("%Y-%m-%d", time.localtime())
                # 设置需要发送的时间
                cmdDaya = (toDay + " " + date + ":00")
                # 控制打印
                # print("cmdDaya:======\n\r %s" % cmdDaya)
                iname = val["api_name"]
                api_id = int(val["api_id"])
                api_hash = val["api_hash"]
                # 群列表
                group_listFor = val["group_list"]
                # 批量添加定时任务的执行命令

                for push in group_listFor:
                    num+=1
                    print(num)
                    pushTo = push["channel_id"]
                    taskid = val["task_guid"]
                    jobCmd["apiName"] = iname
                    jobCmd["apiId"] = api_id
                    jobCmd["apiHash"] = api_hash
                    jobCmd["to"] = pushTo
                    jobCmd["msg"] = val["msg"]
                    jobCmd["method"] = val["method"]
                    jobCmd["taskid"] = taskid
                    jobCmd["id"] = md5(taskid)
                    jobCmd["time"] = cmdDaya
                    jobList.append(jobCmd)
        print([
            '任务数量',
            len(jobList)
        ])
        return jobList
