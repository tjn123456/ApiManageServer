# -*- coding: utf-8 -*-

from flask_restful import request
import sys
sys.path.append('..')
from app.main.basic import base
from app.main.basic import beehive_redis

def user_valid():
    token = request.headers['token']
    print(token)
    print("####################################################")
    try:
        user_str = base.decrypt(token)
    except (BaseException) as e:
        print(e,"无效token")
        return False
    username = user_str.split(',')[0]
    print(username)
    if beehive_redis.gettoken(username,token):
        return True
    else:
        return False
