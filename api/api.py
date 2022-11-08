# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
# 扩展模块
from functools import wraps
from werkzeug.utils import secure_filename

import json

from tools.http import ok, req, error, loadOk, loadErr
from tools.redis_con import RedisCon

from model.dbconf import app

from rq import Queue
from rq.job import Job
from worker import conn, runWorker

from job.job_rq import JobRq

from model.user import User
from model.user_account import UserAccount
from model.user_account_friend import UserAccountFriend
from model.user_account_group import UserAccountGroup
from model.task import Task
from model.task_msg import TaskMsg
from model.user_account_group_user import UserAccountGroupUser

from dao.task_dao import TaskDao
from dao.user_dao import UserDao
from dao.task_private_dao import TaskPrivateDao
from dao.msg_dao import MsgDao

# 建立与Redis server的连接并初始化一个队列
q = Queue(connection=conn)

ruser = RedisCon('user')  # 新建队列名为rq


def pushQueue(jobData={}, jobId=None):
    q.enqueue_call(runWorker, args=(jobData,), job_id=jobId, result_ttl=500)
    return True


executor = ThreadPoolExecutor(6)


def checkAuth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        authorization = request.headers.get('Authorization')
        if authorization:
            strLen = len(authorization)
            if strLen == 32:
                jsonStr = ruser.getStr(name=authorization)
                if jsonStr == None:
                    return error("Unsafe Error", 400)
                kwargs["users"] = json.loads(jsonStr)
                return func(*args, **kwargs)
        else:
            return error("is login the unsafe error", 400)

    return decorated_function


# upload id file
def allowed_file(filename):
    ext = {'session'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ext


@app.route('/')
def index():
    return ok()


@app.route('/v1/test', methods=['GET'])
def vtest():
    return ok("ok")


@app.route('/v1/login', methods=['POST'])
def login():
    data = req()
    dao = UserDao()
    loginData = dao.login(email=data['email'], passwd=data["passwd"], remote_addr=request.remote_addr, ruser=ruser)
    if loginData:
        return ok("ok", loginData)
    else:
        return error("账户或密码有误..")


@app.route('/v1/out', methods=['GET'])
@checkAuth
def out(users=None):
    ruser.delStr(users["token"])
    return ok("ok")


@app.route('/job/check')
@checkAuth
def jobCheck(users=None):
    jobId = request.args.get("jobId")
    job = Job.fetch(jobId, connection=conn)  # 获取根据job_id获取任务的返回值
    if job.is_finished:  # 检验是否完成
        return ok("ok", {"result": job.result})
    else:
        return error("Wait..")


@app.route('/v1/task/private/list', methods=['GET'])
@checkAuth
def task_private_list(users=None):
    page = request.args.get("page")
    if page == None:
        page = 1
    else:
        page = int(page)
    tp = TaskPrivateDao(userId=users["user_id"])
    tp.page = page
    list = tp.getTaskPrivateList()
    return ok("ok", list)


@app.route('/v1/task/private/list/log', methods=['GET'])
@checkAuth
def task_private_list_log(users=None):
    page = request.args.get("page")
    guid = request.args.get("id")
    if page == None:
        page = 1
    else:
        page = int(page)
    tp = TaskPrivateDao(taskId=guid)
    tp.page = page
    list = tp.getTaskPrivateListLog()
    return ok("ok", list)


@app.route('/v1/task/private/add', methods=['POST'])
@checkAuth
def task_private_add(users=None):
    data = req()
    guid = data["guid"]
    if len(data) > 2:
        tp = TaskPrivateDao()
        data["user_id"] = users["user_id"]
        if guid == "0":
            stu = tp.addTaskPrivate(data=data)
            jobRq = JobRq(uid=users["user_id"])
            jobData = jobRq.taskPrivate(taskId=stu)
            ext = jobData['ext']
            pushQueue(jobData=jobData, jobId=ext['jobId'])
            return ok(msg="ok")

    return error("编辑失败")


@app.route('/v1/task/private/edit', methods=['POST'])
@checkAuth
def task_private_edit(users=None):
    data = req()
    if len(data) > 2:
        tp = TaskPrivateDao()
        tp.editTaskPrivate(data=data)
        return ok()
    return error("编辑失败")


@app.route('/v1/task/private/one', methods=['GET'])
@checkAuth
def task_private_one(users=None):
    guid = request.args.get("guid")
    tp = TaskPrivateDao(taskId=guid)
    dat = tp.getOne()
    return ok(idata=dat)


@app.route('/v1/task/private/del', methods=['GET'])
@checkAuth
def task_private_del(users=None):
    guid = request.args.get("guid")
    tp = TaskPrivateDao(taskId=guid)
    tp.delAll()
    return ok()


@app.route('/v1/task/private/start', methods=['GET'])
@checkAuth
def task_private_start(users=None):
    guid = request.args.get("guid")
    print(guid)
    tp = TaskPrivateDao(taskId=guid)
    tp.startTask()
    return ok()


@app.route('/v1/task/private/stop', methods=['GET'])
@checkAuth
def task_private_stop(users=None):
    guid = request.args.get("guid")
    print(guid)
    tp = TaskPrivateDao(taskId=guid)
    tp.stopTask()
    return ok()


@app.route('/v1/user/list', methods=['GET'])
@checkAuth
def user_list(users=None):
    role = users["role"]
    if role == 1:
        page = request.args.get("page")
        if page == None:
            page = 1
        else:
            page = int(page)

        u = User(status=1, page=page)
        list = u.byListPage()
        return ok("ok", list)
    else:
        return error("Parameter error")


@app.route('/v1/user/details', methods=['GET'])
@checkAuth
def user_details(users=None):
    role = users["role"]
    if role == 1:
        guid = request.args.get("guid")
        u = User(guid=guid)
        details = u.byGuidDetails()
        if details == None:
            details = {}
        return ok("ok", details)


@app.route('/v1/user/edit', methods=['POST'])
@checkAuth
def user_edit(users=None):
    data = req()
    itype = data["type"]
    stu = None
    role = users["role"]
    umodel = User()
    if itype == 'add' or role == 1:
        if data["guid"] == 0:
            umodel.email = data["email"]
            umodel.password = data["passwd"]
            umodel.tgNumber = data["tgNumber"]
            umodel.tgGroupNumber = data["tgGroupNumber"]
            umodel.taskNumber = data["taskNumber"]
            byEmailDetails = umodel.byEmailDetails()
            if byEmailDetails:
                return error("账户已经存在..")
            else:
                stu = umodel.insert()
    elif itype == 'info' or role == 1:
        umodel.tgNumber = data["tgNumber"]
        umodel.tgGroupNumber = data["tgGroupNumber"]
        umodel.taskNumber = data["taskNumber"]
        stu = umodel.update()
    elif itype == 'passwd':
        umodel.guid = data["guid"]
        umodel.password = data["passwd"]
        stu = umodel.updatePasswd()
    if stu == None:
        return ok("ok")

    return error("Parameter error")


@app.route('/v1/user/edit/passwd', methods=['POST'])
@checkAuth
def user_edit_passwd(users=None):
    # print(users)
    data = req()
    umodel = User()
    role = users["role"]
    userId = users["user_id"]
    if role == 1 or userId == data["guid"]:
        umodel.guid = data["guid"]
        umodel.password = data["passwd"]
        stu = umodel.updatePasswd()
        if stu == None:
            return ok("ok")
    return error("Parameter error")


@app.route('/v1/user/del', methods=['GET'])
@checkAuth
def user_del(users=None):
    guid = request.args.get("guid")
    stu = False
    role = users["role"]
    if role != 1:
        return error("Parameter error")

    if guid != 0:
        umodel = User(guid=guid)
        stu = umodel.delete()

    if stu == None:
        return ok("删除成功")
    else:
        return error("已删除")

    return error("删除失败,服务器繁忙")


@app.route('/v1/tg/account/list', methods=['GET'])
@checkAuth
def tg_account_list(users=None):
    uid = request.args.get("uid")
    page = request.args.get("page")
    status = request.args.get("status")

    stu = 0
    if type(status) == str:
        stu = int(status)
    else:
        stu = status

    if page == None:
        page = 1
    else:
        page = int(page)

    if stu > 3:
        return error("参数错误.")

    accm = UserAccount(page=page, user_id=uid)
    if stu == 1:
        list = accm.byListPage()
        return ok("ok", list)
    elif stu > 1 or stu < 3:
        list = accm.byStatusListPage(is_activation=stu)
        return ok("ok", list)
    else:
        return error("请求有误..")


@app.route('/v1/tg/account/join/group', methods=['POST'])
@checkAuth
def tg_account_join_group(users=None):
    dat = req()
    try:
        tid = dat["tid"]
        groupLink = dat["groupLink"]
        uid = users["user_id"]
        if len(groupLink) > 0:
            tmp = groupLink.split()
            if len(tmp) > 0:
                dao = UserDao()
                jobDat = dao.joinGroup(tid=tid, uid=uid, groupLink=tmp)
                print(jobDat)
                if len(jobDat) > 0:
                    jobId = pushQueue(jobDat)
                    return ok("ok", {"jobId": jobId})
    except BaseException as err:
        print(err)
        return error(msg=err)
    return ok()


from tools.so import so

@app.route('/v1/tg/account/so', methods=['GET'])
# @checkAuth
def tg_account_so(users=None):
    keys = request.args.get("keys")
    # userId = users["user_id"]
    # try:
    #     uriList = so(key=keys)
    #     return ok(idata=uriList)
    # except BaseException as err:
    #     return error(msg=err)
    uriList = so(key=keys)
    # print(uriList)
    return ok(idata=uriList)


@app.route('/v1/tg/account/check', methods=['GET'])
@checkAuth
def tg_account_check(users=None):
    uid = users["user_id"]
    try:
        dao = UserDao()
        jobDat = dao.checkAccount(uid=uid)
        if len(jobDat) > 0:
            jobId = pushQueue(jobDat)
            return ok("ok", {"jobId": jobId})
    except BaseException as err:
        print(err)
    return ok()


@app.route('/v1/tg/account/load', methods=['POST'])
@checkAuth
def tg_account_load(users=None):
    userId = users["user_id"]
    sessionDir = os.path.abspath(os.path.dirname(__file__)) + "/session/"
    if 'file' not in request.files:
        return loadErr(msg="key file")
    f = request.files['file']
    dao = UserDao(userId=userId)
    if f.filename == '':
        return loadErr(msg="No selected file")
    if f and allowed_file(f.filename):
        try:
            filename = f.filename.split('.')
            phone = None
            if len(filename) == 2:
                phone = filename[0]
            f.save(os.path.join(sessionDir, secure_filename(f.filename)))
            dao.loadAddAcc(phone=phone)
            return loadOk()
        except BaseException as err:
            return loadErr(msg=err)
    else:
        return loadErr(msg="文件格式不正确.")


@app.route('/v1/tg/account/edit', methods=['POST'])
@checkAuth
def tg_account_edit(users=None):
    data = req()
    stu = None
    userId = users["user_id"]
    if data["guid"] == 0 or data["guid"] == "0":
        uam = UserAccount(user_id=userId,
                          api_id=data["api_id"],
                          api_hash=data["api_hash"],
                          api_name=data["api_name"],
                          api_certificate=data["api_certificate"],
                          phone=data["phone"],
                          username=data["username"]
                          )
        stu = uam.insert()
    else:
        uam = UserAccount(guid=data["guid"],
                          api_id=data["api_id"],
                          api_hash=data["api_hash"],
                          api_name=data["api_name"],
                          api_certificate=data["api_certificate"],
                          phone=data["phone"],
                          username=data["username"])
        stu = uam.update()
    if stu == None:
        return ok("ok")
    else:
        return error("编辑失败")


@app.route('/v1/tg/account/get/code', methods=['POST'])
@checkAuth
def tg_account_get_code(users=None):  # 获取账号验证码
    data = req()
    uid = data["uid"]
    tid = data["tid"]
    jobRq = JobRq(uid=uid, tid=tid)
    jobData = jobRq.getCode()
    ext = jobData['ext']
    pushQueue(jobData=jobData, jobId=ext['jobId'])
    return ok(msg="ok")


@app.route('/v1/tg/account/details', methods=['GET'])
@checkAuth
def tg_account_details(users=None):
    guid = request.args.get("guid")
    if guid:
        u = UserAccount(guid=guid)
        details = u.byGuidDetails()
        return ok("ok", details)
    return error("not data", 201)


@app.route('/v1/tg/account/status', methods=['POST'])
@checkAuth
def tg_account_status(users=None):
    data = req()
    stu = False
    if data["guid"] != 0:
        uam = UserAccount(guid=data["guid"], status=data["status"])
        stu = uam.upStatus()
    if stu == None:
        return ok("更新成功")
    else:
        return error("更新失败")

    return error("更新失败,服务器繁忙")


@app.route('/v1/tg/account/get/group', methods=['POST'])
@checkAuth
def tg_account_get_group(users=None):
    data = req()
    uid = data["uid"]
    tid = data["tid"]
    jobRq = JobRq(uid=uid, tid=tid)
    jobData = jobRq.getGroup()
    ext = jobData['ext']
    pushQueue(jobData=jobData, jobId=ext['jobId'])
    return ok(msg="ok")


@app.route('/v1/tg/account/activation', methods=['POST'])
@checkAuth
def tg_account_activation(users=None):
    data = req()
    tid = data["guid"]
    uid = data["uid"]
    code = data["code"]
    jobRq = JobRq(uid=uid, tid=tid)
    jobData = jobRq.webActivationLogin(code=code)
    ext = jobData['ext']
    pushQueue(jobData=jobData, jobId=ext['jobId'])
    return ok(msg="ok")


@app.route('/v1/tg/account/search/username', methods=['POST'])
@checkAuth
def tg_account_search_username(users=None):
    data = req()
    uid = data["uid"]
    username = data["username"]
    if uid or username:
        ua = UserAccount(user_id=uid)
        list = ua.handleSearchName(username=username)
        return ok("ok", list)
    return error("not data", 201)


@app.route('/v1/tg/account/new/group', methods=['POST'])
@checkAuth
def tg_account_new_group(users=None):
    data = req()
    print(data)
    uid = data["uid"]
    tid = data["tid"]
    name = data["name"]
    usersList = data["users"]
    ua = UserAccount(guid=tid, new_group_name=name, new_group_list=usersList)
    reqs = ua.upNewGroup()
    if reqs:
        jobRq = JobRq(uid=uid, tid=tid)
        jobData = jobRq.newGroup()
        ext = jobData['ext']
        pushQueue(jobData=jobData, jobId=ext['jobId'])
        return ok(msg="ok")
    return error("创建失败")


@app.route('/v1/tg/account/group/extract', methods=['POST'])
@checkAuth
def tg_account_group_extract(users=None):
    data = req()
    uid = data["uid"]
    tid = data["tid"]
    tgid = data["tgid"]

    if tid:
        jobRq = JobRq(uid=uid, tid=tid)
        jobData = jobRq.getExtractGroup(tgGroupId=tgid)
        ext = jobData['ext']
        pushQueue(jobData=jobData, jobId=ext['jobId'])
        return ok(msg="ok")
    return error("not data", 201)


@app.route('/v1/tg/account/group/push/msg', methods=['POST'])
@checkAuth
def tg_account_group_push_msg(users=None):
    data = req()
    uid = data["uid"]
    tid = data["tid"]
    to = data["to"]
    msg = data["msg"]
    jobRq = JobRq(uid=uid, tid=tid)
    jobData = jobRq.pushGroupOneMsg(to=to, msg=msg)
    ext = jobData['ext']
    pushQueue(jobData=jobData, jobId=ext['jobId'])
    return ok(msg="ok")


@app.route('/v1/tg/account/private/push/msg', methods=['POST'])
@checkAuth
def tg_account_private_push_msg(users=None):
    data = req()
    uid = data["uid"]
    tid = data["tid"]
    to = data["to"]
    msg = data["msg"]
    jobRq = JobRq(uid=uid, tid=tid)
    jobData = jobRq.pushPrivateOneMsg(to=to, msg=msg)
    ext = jobData['ext']
    pushQueue(jobData=jobData, jobId=ext['jobId'])
    return ok(msg="ok")


@app.route('/v1/tg/account/group/user/list', methods=['GET'])
@checkAuth
def tg_account_group_user_list(users=None):
    page = request.args.get("page")
    if page == None:
        page = 1
    else:
        page = int(page)
    uagid = request.args.get("uagid")
    if uagid:
        ul = UserAccountGroupUser(user_account_group_id=uagid, page=page)
        ulist = ul.byListPage()
        return ok("ok", ulist)
    return error("not data", 201)


@app.route('/v1/tg/account/group/user/all', methods=['GET'])
@checkAuth
def tg_account_group_user_all(users=None):
    page = request.args.get("page")
    if page == None:
        page = 1
    else:
        page = int(page)

    uid = request.args.get("uid")
    if uid:
        ul = UserAccountGroupUser(user_id=uid, page=page)
        ulist = ul.byUserAllPage()
        return ok("ok", ulist)
    return error("not data", 201)


@app.route('/v1/tg/friend/edit', methods=['POST'])
@checkAuth
def friend_edit(users=None):
    data = req()
    stu = None
    if data["guid"] == 0:
        model = UserAccountFriend(key=data["key"],
                                  user_id=data["user_id"],
                                  user_account_id=data["user_account_id"],
                                  account_id=data["account_id"],
                                  account_name=data["account_name"],
                                  name=data["name"],
                                  avatar=data["avatar"]
                                  )
        stu = model.insert()
    else:
        model = UserAccountFriend(guid=data["guid"], key=data["key"],
                                  user_id=data["user_id"],
                                  user_account_id=data["user_account_id"],
                                  account_name=data["account_name"],
                                  name=data["name"],
                                  avatar=data["avatar"])
        stu = model.update()
    if stu == None:
        return ok("ok")
    else:
        return error("编辑失败")


@app.route('/v1/tg/group/edit', methods=['POST'])
@checkAuth
def group_edit(users=None):
    data = req()
    stu = None
    if data["guid"] == 0:
        model = UserAccountGroup(
            user_id=data["user_id"],
            user_account_id=data["user_account_id"],
            channel_id=data["channel_id"],
            channel_title=data["channel_title"],
            channel_username=data["channel_username"],
            channel_access_hash=data["channel_access_hash"]
        )
        stu = model.insert()
    else:
        model = UserAccountGroup(
            guid=data["guid"],
            channel_id=data["channel_id"],
            channel_title=data["channel_title"],
            channel_username=data["channel_username"],
            channel_access_hash=data["channel_access_hash"]
        )
        stu = model.update()
    if stu == None:

        return ok("ok")
    else:
        return error("编辑失败", 201)


@app.route('/v1/tg/group/list', methods=['GET'])
@checkAuth
def group_list(users=None):
    user_account_id = request.args.get("user_account_id")
    userId = users["user_id"]
    lenUaId = len(user_account_id)
    if lenUaId > 38:
        return error("请求无效..")
    if user_account_id == '0':
        group = UserAccountGroup()
        list = group.byUserIdList(user_id=userId)
    else:
        group = UserAccountGroup()
        list = group.byUserAccountIdList(user_account_id=user_account_id)
    return ok("ok", list)


@app.route('/v1/tg/group/list/so/acc', methods=['GET'])
@checkAuth
def group_list_so_acc(users=None):
    userId = users["user_id"]
    ua = UserAccount()
    ilist = ua.byUserIdList(userId=userId)
    return ok("ok", ilist)


@app.route('/v1/task/list', methods=['GET'])
@checkAuth
def task_list(users=None):
    page = request.args.get("page")
    if page == None:
        page = 1
    else:
        page = int(page)
    task = Task(status=1, user_id=users["user_id"], page=page)
    list = task.byUidListPage()
    return ok("ok", list)


@app.route('/v1/task/list/msg', methods=['GET'])
@checkAuth
def task_list_msg(users=None):
    task_id = request.args.get("task_id")
    if task_id == None:
        return error("数据错误..")
    imsg = TaskMsg(status=1, task_id=task_id)
    list = imsg.byTaskIdList()
    return ok("ok", list)


@app.route('/v1/task/details', methods=['GET'])
@checkAuth
def task_details(users=None):
    guid = request.args.get("guid")
    task = Task(guid=guid)
    details = task.byGuidDetails()
    if details == None:
        details = {}
    else:
        imsg = TaskMsg(task_id=guid)
        iMsgList = imsg.byTaskIdList()
        details["msg_list"] = iMsgList
    return ok("ok", details)


@app.route('/v1/task/del', methods=['GET'])
@checkAuth
def task_del(users=None):
    guid = request.args.get("guid")
    userId = users["user_id"]
    if userId.strip() == '':
        userId = request.args.get("userId")

    dao = TaskDao(taskId=guid, userId=userId)
    dao.byTaskIdInUidDelMsg()
    return ok("删除成功")


@app.route('/v1/task/msg/del', methods=['GET'])
@checkAuth
def task_msg_del(users=None):
    msgId = request.args.get("msgId")
    try:
        dao = TaskDao()
        dao.byMsfIdMsgDel(msgId=msgId)
        return ok("删除成功")
    except BaseException as err:
        print(err)
        return error("删除失败")


@app.route('/v1/task/group/edit', methods=['POST'])
@checkAuth
def task_group_edit(users=None):
    data = req()
    dao = TaskDao()
    stu = dao.addTask(data=data)
    if stu == True:
        return ok("任务创建成功")
    else:
        return error("创建任务失败.")


@app.route('/v1/task/group/start', methods=['GET'])
@checkAuth
def task_group_start(users=None):
    guid = request.args.get("guid")
    uid = users["user_id"]
    dao = TaskDao(taskId=guid, userId=uid)
    dao.start()
    return ok()


@app.route('/v1/task/group/stop', methods=['GET'])
@checkAuth
def task_group_stop(users=None):
    guid = request.args.get("guid")
    uid = users["user_id"]
    dao = TaskDao(taskId=guid, userId=uid)
    dao.stop()
    return ok()


@app.route('/v1/msg/list', methods=['GET'])
@checkAuth
def msg_list(users=None):
    userId = users["user_id"]
    dao = MsgDao(userId=userId)
    list = dao.getUserIdList()
    if list != None:
        return ok("ok", list)
    return ok()


@app.route('/v1/msg/count', methods=['GET'])
@checkAuth
def msg_count(users=None):
    userId = users["user_id"]
    dao = MsgDao(userId=userId)
    dat = dao.getUserIdCountAOne()
    return ok(msg="ok", idata=dat)


@app.route('/v1/msg/read', methods=['GET'])
@checkAuth
def msg_read(users=None):
    guid = request.args.get("guid")
    dao = MsgDao(msgId=guid)
    dat = dao.byGuidReadUp()
    return ok(msg="ok", idata=dat)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8091, debug=True)
