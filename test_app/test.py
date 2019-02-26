# -*- coding: utf-8 -*-

from requests import post,get
import time
import sys
sys.path.append("..")
from app.model_path import Fun_path

# login_url = "http://127.0.0.1:5001/login"
# #临时token = "dGpuLGUxMGFkYzM5NDliYTU5YWJiZTU2ZTA1N2YyMGY4ODNl"
# login_data = {"username":'tjn',"password":"123456"}
# longtask_url = 'http://127.0.0.1:5001/re'
# getid_url = 'http://127.0.0.1:5001/task/'
# url = "https://www.baidu.com"
# data = {'':''}
# header = {'token':'dGpuLGUxMGFkYzM5NDliYTU5YWJiZTU2ZTA1N2YyMGY4ODNl'}
# res = get(url,data)
# #login_res = post(login_url,login_data)
#
# print(res.text)


#
# from redis import Redis, ConnectionPool
#
#
# pool = ConnectionPool(host='127.0.0.1', port='6379',max_connections=1000)
# r = Redis(connection_pool=pool)
#
# r.set('aaa','bbb')
# data = Fun_path.query.filter_by(classify=1).all()
# list = []
# son = {}
# for i in data:
#     dict = {'id': i.id, 'text': i.name, 'value': i.fun_id, 'item': ''}
#     if i.fa_id:
#         dict2 = {'id': i.id, 'text': i.name, 'value': i.fun_id}
#         son[i.fa_id] = dict2
#     else:
#         list.append(dict)
list = [{'id': 1, 'text': '一级测试', 'value': '', 'pid': ''}, {'id': 2, 'text': '二级测试', 'value': '', 'pid': ''}, {'id': 3, 'text': '二级测试', 'value': '1', 'pid': '1'}, {'id': 4, 'text': '二级测试2', 'value': '2', 'pid': '1'}, {'id': 5, 'text': '222', 'value': '', 'pid': ''}, {'id': 6, 'text': '权威', 'value': '3', 'pid': '5'}, {'id': 7, 'text': '333', 'value': '4', 'pid': '1'}, {'id': 8, 'text': '444', 'value': '5', 'pid': '1'}, {'id': 9, 'text': '5555', 'value': '6', 'pid': '1'}, {'id': 10, 'text': '666', 'value': '7', 'pid': '1'}, {'id': 11, 'text': '777', 'value': '8', 'pid': '1'}, {'id': 12, 'text': '88888', 'value': '9', 'pid': '1'}, {'id': 13, 'text': '99999', 'value': '10', 'pid': '1'}, {'id': 14, 'text': '1010101', 'value': '11', 'pid': '1'}, {'id': 15, 'text': '12121212121', 'value': '12', 'pid': '1'}, {'id': 16, 'text': '131313131313', 'value': '13', 'pid': '1'}, {'id': 17, 'text': '141414141', 'value': '14', 'pid': '1'}, {'id': 18, 'text': '15151515', 'value': '15', 'pid': '1'}, {'id': 19, 'text': '117171717', 'value': '16', 'pid': '1'}, {'id': 20, 'text': '好尴尬', 'value': '17', 'pid': '1'}, {'id': 21, 'text': '帮你们', 'value': '18', 'pid': '1'}, {'id': 22, 'text': '第三方第三方', 'value': '19', 'pid': '1'}, {'id': 23, 'text': '阿萨德撒所', 'value': '20', 'pid': '1'}, {'id': 24, 'text': '渡水复渡水', 'value': '21', 'pid': '1'}, {'id': 25, 'text': 'bala', 'value': '22', 'pid': '2'}, {'id': 26, 'text': 'bala', 'value': '23', 'pid': '2'}]

# son = {'0':{'id': 1, 'text': '一级测试', 'value': '',},
#        '0':{'id': 2, 'text': '二级测试', 'value': '',},
#        '0':{'id': 5, 'text': '222', 'value': '',}
#        '1': {'id': 24, 'text': '渡水复渡水', 'value': '21'},
#        '5': {'id': 6, 'text': '权威', 'value': '3'},
#        '2': {'id': 26, 'text': 'bala', 'value': '23'}
#        }

id = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']

#将所有的子目录格式改为{pid:{obj}}
di = {}
for i in id:
    re = []
    for j in list:
        if j['pid'] == i:
            re.append(j)
    if re !=[]:
        di[i] = re

#print(di)

#将子目录放入腹肌目录内
for i in list:
    for j in test.keys():
        if i['id'] == str(j):
            i['item']=test[str(j)]
#print(list)
#将重复的子目录清除
list = [i for i in list if i['pid']=='']
print(list)

