# -*- coding: utf-8 -*-
'''
    beehive对redis的操作
    settoken将token存入redis有效期为24小时
    gettoken判断当前用户token是否失效，未失效则更新效期为24小时，失效则返回
'''
from redis import Redis, ConnectionPool
import sys
sys.path.append("....")
from config import redis_url


pool = ConnectionPool(host=redis_url["url"], port=redis_url["port"],max_connections=1000)
r = Redis(connection_pool=pool)

def settoken(username,token):
    #token有效期为12小时
    r.set(username,token,43200)

def gettoken(username,token):
    #token当被再次获取时会更新12小时有效期
    #print(r.get(username))
    if r.get(username) == token.encode():
        r.set(username,token,43200)
        return True
    else:
        return False
