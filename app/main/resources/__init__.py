# -*- coding: utf-8 -*-

from flask_restful import request
from ..basic import base
from ..basic import beehive_redis

def user_valid():
    try:
        token = request.headers['token']
        print(token)
        print("####################################################")
        user_str = base.decrypt(token)
        print(user_str)
    except (BaseException) as e:
        print(e,"无效token")
        return False
    username = user_str.split(',')[0]
    print(username)
    if beehive_redis.gettoken(username,token):
        return True
    else:
        return False
