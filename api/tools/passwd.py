# !/usr/bin/env python
# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash


def createPasswd(passwd):
    return generate_password_hash(passwd)


def checkPasswd(checkPasswd, passwd):
    return check_password_hash(checkPasswd, passwd)
