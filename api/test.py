# !/usr/bin/env python
# -*- coding:utf-8 -*-
from job.task_group import JobTaskGroup

from job.job_rq import JobRq
import json

from tools.redis_con import RedisCon
from model.task_msg import TaskMsg

raps = RedisCon('aps')
msg = TaskMsg()

list = msg.jobMsg()
raps.setStr("aps", json.dumps(list))

print(raps.getStr("aps"))