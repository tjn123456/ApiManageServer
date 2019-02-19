# -*- coding: utf-8 -*-
from requests import post,get
import time
"""测试接口使用：
    模拟接口请求"""
url = "http://127.0.0.1:5001/ApiPath"
data1 = {"api_id":'1',"apicase_id":"21"}
data2 = {"api_id":'0',"apifa_id":"0","api_name":"father"}
data3 = {"api_id":'',"apifa_id":"1","api_name":"son"}
#reqdata = {'req':'get','url':'http://www.baidu.com'}
# headers = {
#     "Accept":"application/json,text/javascript,*/*; q=0.01",
#     "Origin":"null",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "Content-Type":"application/x-www-form-urlencoded,charset=UTF-8",
#     "Accept-Encoding":"gzip, deflate, br",
#     "Accept-Language":"zh-CN,zh;q=0.9"
#     }
res = get(url=url)
print(res)

# # from redis import Redis, ConnectionPool
# # from time import sleep
# # from app.main.basic import base
# '''
# Host: 127.0.0.1:5001
# Connection: keep-alive
# Content-Length: 418
# Accept: application/json, text/javascript, */*; q=0.01
# Origin: null
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# '''


# username = 'tianjiannan'
# password = 'balabalabala'
# token_str = username+','+password
# token = base.encrypt(token_str)
# print(token)
#
# token_str = base.decrypt(token)
# user = token_str.split(',')[0]
# print(user)


# 1、插入token和有效时间
# 2、查询token（问题在于查询方法需要输入key，这样token需要存在key中）
#     解决方案：插入token时插入username+token的加密，查询时拆解加密的到username做为key进行查询token并验证
# 3、查询正确后更新token时间




