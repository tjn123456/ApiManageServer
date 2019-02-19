# -*- coding: utf-8 -*-

from requests import post,get
import time

login_url = "http://127.0.0.1:5001/login"
#临时token = "dGpuLGUxMGFkYzM5NDliYTU5YWJiZTU2ZTA1N2YyMGY4ODNl"
login_data = {"username":'tjn',"password":"123456"}
longtask_url = 'http://127.0.0.1:5001/re'
getid_url = 'http://127.0.0.1:5001/task/'
url = "https://www.baidu.com"
data = {'':''}
header = {'token':'dGpuLGUxMGFkYzM5NDliYTU5YWJiZTU2ZTA1N2YyMGY4ODNl'}
res = get(url,data)
#login_res = post(login_url,login_data)

print(res.text)


#
# from redis import Redis, ConnectionPool
#
#
# pool = ConnectionPool(host='127.0.0.1', port='6379',max_connections=1000)
# r = Redis(connection_pool=pool)
#
# r.set('aaa','bbb')
