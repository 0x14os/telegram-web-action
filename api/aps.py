# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_apscheduler import APScheduler
import json
from rq import Queue

from model.dbconf import app

from tools.help import md5
from tools.http import ok, error
from worker import conn, runWorker
from job.job_rq import JobRq
from tools.redis_con import RedisCon

from dao.task_dao import TaskDao
from works.task_private_works import TaskPrivateWork

aps = APScheduler(app=app)

# 建立与Redis server的连接并初始化一个队列
q = Queue(connection=conn)
raps = RedisCon('aps')


def pushQueue(jobData={}):
    job = q.enqueue_call(runWorker, args=(jobData,), result_ttl=100)
    return job.get_id()


def taskJob(strJson):
    print(strJson)
    jd = json.loads(strJson)
    pushQueue(jd)


def taskPrivateJob(strJson):
    jd = json.loads(strJson)
    pushQueue(jd)


def __privateJobTask(taskId=None):
    # 定时循环发送
    # 每次间隔以定时器作为条件，定时器启动后执行任务
    # 每次启动发送 根据条件发送数量
    task = TaskPrivateWork(taskId=taskId)
    taskDat = task.byTaskIdOne()
    jobId = md5(str(taskId))
    if len(taskDat) > 0:
        timer = int(taskDat["timer"])
        # 队列数据
        job = JobRq()
        jsonDat = job.taskPrivateSend(parameter=taskDat)
        # print("jsonDat",jsonDat)
        strJson = json.dumps(jsonDat)
        aps.add_job(
            id=jobId,
            func=taskPrivateJob,
            trigger='interval',
            seconds=timer,
            # 任务数据
            args=[strJson]
        )
    allNumber()


def __groupMsgTaskJob(taskId=None):
    task = TaskDao(taskId=taskId)
    dat = task.getTaskDetails()
    if len(dat) > 0:
        jobId = md5(str(taskId))
        job = JobRq(uid=dat["user_id"])
        apsJob = job.pushMsgGroupMultiple(taskId=taskId)
        strJson = json.dumps(apsJob)
        timer = int(dat["timer"])
        aps.add_job(
            id=jobId,
            func=taskJob,
            trigger='interval',
            seconds=timer,
            args=[strJson]
        )
        allNumber()


@app.route("/group/add", methods=['GET'])
def addJob():
    taskId = request.args.get("id")
    __groupMsgTaskJob(taskId=taskId)
    return "add"


@app.route("/group/del", methods=['GET'])
def delJob():
    jobId = request.args.get("id")
    jobId = md5(str(jobId))
    jobDat = aps.get_job(id=jobId)
    if jobDat is None:
        return error(msg="not " + jobId)
    else:
        aps.remove_job(id=jobId)
        return ok(idata={"jobId": jobId})


@app.route("/private/add", methods=['GET'])
def addPrivateJob():
    taskId = request.args.get("id")
    print(taskId)
    __privateJobTask(taskId=taskId)
    return "add"


@app.route("/private/del", methods=['GET'])
def delPrivateJob():
    taskId = request.args.get("id")
    print(taskId)
    jobId = md5(str(taskId))
    jobDat = aps.get_job(id=jobId)
    if jobDat is None:
        return error(msg="not " + jobId)
    else:
        aps.remove_job(id=jobId)
        return ok(idata={"jobId": jobId})


@app.route("/all", methods=['GET'])
def allJob():
    jobList = aps.get_jobs()
    print("job number:%d" % len(jobList))
    jobNumber = len(jobList)
    return str(jobNumber)


def allNumber():
    jobList = aps.get_jobs()
    print(jobList)
    jobNumber = len(jobList)
    print("job number:%d" % len(jobList))
    return jobNumber


@app.route("/check", methods=['GET'])
def checkJob():
    taskId = request.args.get("id")
    jobId = md5(str(taskId))
    jobDat = aps.get_job(id=jobId)
    if jobDat is None:
        return error(msg="not " + jobId)
    else:
        aps.remove_job(id=jobId)
        return ok(idata={"jobId": jobId})


def test(jobid=None):
    print(jobid)


@app.route("/test", methods=['GET'])
def testJob():
    taskId = request.args.get("id")
    jobId = md5(str(taskId))
    print(jobId)
    timer = 15
    aps.add_job(
        id=jobId,
        func=test,
        trigger='interval',
        seconds=timer,
        args=[taskId]
    )
    jobList = aps.get_jobs()
    print(jobList)

    return "test"


aps.start()

if __name__ == '__main__':
    # aps.start()
    print("Let us run out of the loop")
    app.run(host="0.0.0.0", port=9896, debug=True)
