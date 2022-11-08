# !/usr/bin/env python
# -*- coding:utf-8 -*-
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import logging
import requests
from requests import exceptions
from tools.help import popen

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='runtime/monitor.logs',
                    filemode='a')
log = logging.getLogger(__name__)

aps_executors = {
    'default': ThreadPoolExecutor(5)
}

aps = BackgroundScheduler(executors=aps_executors)


def stmp():
    print("121212")
    log.info("send to admin email")


def restart():
    log.info("start the restart service tgapi and tgaps")
    popen("systemctl stop tgapi.service")
    popen("systemctl stop tgaps.service")
    popen("systemctl start tgaps.service")
    popen("systemctl start tgapi.service")
    log.info("end the start")
    stmp()


def http():
    try:
        t1 = time.time()
        url = "http://127.0.0.1:8091/v1/test"
        response = requests.get(url, timeout=1)
        t2 = time.time()
    except exceptions.Timeout as e:
        log.warning('请求超时：' + str(e.message))
        restart()
    except exceptions.HTTPError as e:
        log.warning('http请求错误:' + str(e.message))
        restart()
    else:
        # 通过status_code判断请求结果是否正确
        reqTime = '请求耗时%ss' % (t2 - t1)
        log.info(reqTime)
        print(reqTime)
        print(response.text)
        if response.status_code != 200:
            log.warning('请求错误：' + str(response.status_code) + ',' + str(response.reason))


if __name__ == '__main__':
    aps.add_job(http, "interval", seconds=60)
    aps._logger = logging
    aps.start()
    while True:
        print(f'{datetime.now():%H:%M:%S}')
        time.sleep(5)
