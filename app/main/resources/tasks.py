# -*- coding: utf-8 -*-
'''
    该文件为任务模块
    api_task为任务执行中接口自动化任务处理
'''
from flask_restful import reqparse,Resource,request
from ...models2 import Api_info,Apicase_info,Project_task
from requests import post,head,get
import time,datetime,sys
from ..basic.beehive_redis import r as red
sys.path.append("....")
from app import db
import redis
#from rq import Queue
import json

# red = redis.Redis()



def api_task(task_id,apiid_list):
    '''
        异步执行所有测试用例，
        创建一个已project_task.id为名称的redis_hash
        将过程信息存放至redis_hash中，结果存放至数据库
    '''
    # 将所有的数据查询出来，以测试用例为单位放在一个数组中
    req_data = []
    print(apiid_list)
    for api in Api_info.query.filter(Api_info.id.in_(apiid_list)).all():
        print(api.case_id.strip(',').split(','))
        for case in Apicase_info.query.filter(Apicase_info.id.in_(api.case_id.strip(',').split(','))).all():
            test_case = {'apiname':api.name,'casename':case.casename,'httpact':api.httpact,'url':api.requrl,'params':case.params,'headers':case.headers,'bodys':case.bodys,'befun':case.beforefunction,'assfun':case.assertfunction}
            req_data.append(test_case)
    print(req_data)
    '''
        执行所有测试用例
        当前置脚本失败，请求方法错误阻塞计数器+1
        当请求失败，断言失败时失败计数器+1
        执行无报错时成功计数器+1
    '''

    red_name = task_id
    count_log = {'api_success':0,'api_block':0,'api_faild':0,'total':len(req_data),'log':{}}
    # api_success = 0
    # api_block = 0
    # api_faild = 0
    # totle = len(req_data)
    for case in req_data:
        #print(case)
        #这里赋值是为了和单次执行保持一致，这样前置条件和断言脚本才可运行
        requrl,params,bodys,headers = case['url'],case['params'],case['bodys'],case['headers']
        print(requrl)
        try:
            exec(case["befun"])
        except BaseException as e:
            print("in block")
            count_log['api_block'] += 1
            str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+case['apiname']+case['casename']
            count_log['log'][str] = 'block'
            red.hmset(red_name,count_log)
            continue
        if case["httpact"] == 'GET':
            try:
                res = get(url=requrl,params=params,data=bodys,headers=headers).text
            except BaseException as e:
                print(case["apiname"],case["casename"],"in get faild")
                count_log['api_faild'] += 1
                str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
                count_log['log'][str] = 'faild'
                red.hmset(red_name,count_log)
                continue

        elif case["httpact"] == 'POST':
            try:
                print("in post faild")
                res = post(url=requrl,params=params,data=bodys,headers=headers).text
            except BaseException as e:
                count_log['api_faild'] += 1
                str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
                count_log['log'][str] = 'faild'
                red.hmset(red_name, count_log)
                continue

        elif case["httpact"] == 'HEAD':
            try:
                res = head(url=requrl,params=params,data=bodys,headers=headers).text
            except BaseException as e:
                count_log['api_faild'] += 1
                str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
                count_log['log'][str] = 'faild'
                red.hmset(red_name, count_log)
                continue
        else:
            count_log['api_block'] += 1
            str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
            count_log['log'][str] = 'block'
            red.hmset(red_name, count_log)
            continue
        try:
            exec(case["assfun"])
        except BaseException as e:
            print("in assfun faild")
            count_log['api_faild'] += 1
            str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
            count_log['log'][str] = 'faild'
            red.hmset(red_name, count_log)
            continue

        count_log['api_success'] += 1
        str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + case['apiname']+case['casename']
        count_log['log'][str] = 'success'
        red.hmset(red_name, count_log)

        time.sleep(1)
    #将执行结束的count_log保存至数据库
    api_task = Project_task.query.filter(Project_task.id == task_id).first()
    # print(api_task.id)
    # print(json.dumps(count_log))
    api_task.count_log = json.dumps(count_log)
    db.session.add(api_task)
    db.session.commit()
    return 'finish'


parser = reqparse.RequestParser()
parser.add_argument('task_id',type=str)
parser.add_argument('apitask_name',type=str)
parser.add_argument('apitask_detail',type=str)
parser.add_argument('apitask_case',type=str)

def change(dict):
    #获取参数数据中第一个key值
    data = sorted(dict.items())[0][0]
    data = eval(data)
    return data


class Api_Task(Resource):
    def get(self):
        '''
            方法：get
            路径: /ApiTaskInfo
            参数：apitask_id
            业务：在编辑任务时获取任务数据
                使用id值获取任务名称和简介及用例id
        '''
        args = parser.parse_args()
        task_id = args['task_id']
        if task_id :
            try:
                api_task = Project_task.query.filter(Project_task.id == task_id).first()
            except BaseException as e:
                return {'text': 'faild', "data": ["获取任务失败", str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
            data = {'apitask_name':api_task.name,'apitask_detail':api_task.detail,'apitask_case':api_task.testcase}
            return {'text': 'success', "data": data}, 201, {"Access-Control-Allow-Origin": "*"}
        else:
            api_task = Project_task.query.all()
            data = [{'apitask_id':i.id,'apitask_name':i.name,'count':i.count_log} for i in api_task]
            return {'text': 'success', "data": data}, 201, {"Access-Control-Allow-Origin": "*"}


    def post(self):
        '''
            方法：post
            路径: /ApiTaskInfo
            参数：apitask_id,apitask_name,apitask_detail,apitask_case
            业务：创建或修改接口测试任务
                创建时需传入apitask_name,apitask_detail,apitask_case
                修改时需传入apitask_id,apitask_name,apitask_detail,apitask_case
        '''
        data = request.form.to_dict()
        datadict = change(data)
        task_id,name,detail,case_id = datadict["apitask_id"],datadict["apitask_name"], datadict["apitask_detail"], datadict["apitask_case"]
        if task_id == '':
            try:
                task_input = Project_task(name=str(name),testcase=str(case_id), detail=str(detail), status='1')
                db.session.add(task_input)
                db.session.commit()
            except BaseException as e:
                print(str(e))
                return {'text': 'faild', "data": ["创建任务失败",str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
            return {'text':'success',"data":"操作成功"}, 201,{"Access-Control-Allow-Origin": "*"}
        else:
            try:
                api_task = Project_task.query.filter(Project_task.id == task_id).first()
            except BaseException as e:
                return {'text': 'faild', "data": ["修改任务失败", str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
            api_task.name,api_task.testcase,api_task.detail = name,case_id,detail
            db.session.add(api_task)
            db.session.commit()
            return {'text': 'success', "data": "操作成功"}, 201, {"Access-Control-Allow-Origin": "*"}

def add(a,b):
    return a+b

class Api_Runtask(Resource):
    def get(self):
        '''
        方法：get
        路径：/ApiRunTask
        参数：task_id
        业务：获取任务ID进行查询当前任务的执行情况（成功，失败，阻塞，总数，日志）
        '''
        args = parser.parse_args()
        task_id = args['task_id']
        try:
            count_log = red.hgetall(task_id)
            count_log_str = {}
            #将count_log中的二进制类型转换为字符串类型
            for key,value in count_log.items():
                count_log_str[key.decode()] = value.decode()
        except BaseException as e:
            return {'text': 'faild', "data": ["获取任务失败", str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
        return {'text': 'success', 'data': count_log_str}, 201, {"Access-Control-Allow-Origin": "*"}

    def post(self):
        '''
            方法：post
            路径：/ApiRunTask
            参数：task_id
            业务：执行对应id的项目任务
        '''
        args = parser.parse_args()
        task_id = args['task_id']
        api_task_instance = Project_task.query.filter(Project_task.id == task_id).first()
        apiid_list = eval(api_task_instance.testcase)
        try:
            job = api_task(task_id,apiid_list)
            #job = q.enqueue(api_task,*[apiid_list,task_id])
        except BaseException as e:
            print(e)
            return {'text': 'faild', "data": ["执行任务失败", str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
        return {'text': 'success', "data": "执行任务成功"}, 201, {"Access-Control-Allow-Origin": "*"}



