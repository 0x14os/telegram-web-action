# !/usr/bin/env python
# -*- coding:utf-8 -*-

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime, timedelta
import logging

from tools.help import popen

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.txt',
                    filemode='a')
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


class TaskAps:
    add = None
    job = None
    func = None
    cmd = None
    time = None
    aps = None
    _aps_executors = {}
    task_id = None
    itype = 'interval'

    def __init__(self, func=None, add=None, job=None, cmd=None, time=None, task_id=None):
        self.add = add
        self.job = job
        self.func = func
        self.cmd = cmd
        self.time = time
        self.task_id = task_id

    def init(self):
        self.aps = BackgroundScheduler(executors=self._aps_executors)

    def config(self):
        self._aps_executors = {
            'default': ThreadPoolExecutor(10)
        }

    # 添加任务
    def addJob(self):
        self.aps.add_job(self.func, self.itype, minutes=2, id=self.task_id)

    # 删除任务
    def removeJob(self):
        self.aps.remove_job(self.func)

    # 暂定任务
    def pauseJob(self):
        self.aps.pause_job(self.func)

    # 恢复任务
    def resumeJob(self):
        self.aps.resume_job(self.func)

    # 停止定时器
    def down(self):
        self.aps.shutdown()

    def start(self):
        self.aps._logger = logging
        self.aps.start()
