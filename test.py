# -*- coding: utf-8 -*-
from requests import post,get
import time
"""测试接口使用：
    模拟接口请求"""
url = "http://127.0.0.1:5001/ApiPath"
data1 = {"api_name":'新建目录',"add_type":"1","apifa_id":"2"}
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
res = post(url=url,data=data1)
print(res.json())






