# -*- coding: utf-8 -*-
import sys
from flask_restful import reqparse,Resource,request
import json
from flask import Request
import requests
from requests import get,post,head
from ...models2 import Api_info,Apicase_info
from ...model_path import Fun_path
from ..basic import base
sys.path.append("....")
from app import db

parser = reqparse.RequestParser()
parser.add_argument('api_id',type=str)
parser.add_argument('api_name',type=str)
parser.add_argument('operation',type=str)
parser.add_argument('apicasename',type=str)
parser.add_argument('apicase_id',type=str)
parser.add_argument("api_tree_id",type=str)


def change(dict):
    #获取参数数据中第一个key值
    data = sorted(dict.items())[0][0]
    data = eval(data)
    return data

def get_args(list):
    #拆解列表返回参数字典
    valdict = {}
    for (a,b,c) in list:
        valdict[a] = b
    return valdict

class api_single(Resource):
    '''
        方法：post
        路径: /apisingle
        参数：requrl--获取被测接口的url,
            params--获取url后拼接的参数,
            httpaction--获取请求的方法,
            headers--获取被测接口的头部信息,
            bodys--获取被测接口的主体,
            befun--获取前置脚本,
            assfun--获取断言脚本,
            bekeys--获取前置调试关键字,
            asskeys--获取断言调试关键字
        业务：api_id所获取的接口id
        apicase_id所获取的用例id
        逻辑：获取接口数据只需要传api_id
        获取用例数据需要传递api_id,apicase_id
    '''
    #断言部分未完成
    def post(self):
        # args = parser.parse_args()
        data = request.form.to_dict()
        datadict = change(data)
        requrl,params,httpaction,headers,bodys = datadict["requrl"],datadict["params"],datadict["httpaction"],datadict["headers"],datadict["bodys"]
        befun,assfun= datadict['befun'],datadict['assfun']
        params = get_args(params)
        bodys = get_args(bodys)
        headers = get_args(headers)
        #执行前置脚本
        try:
            exec(befun)
        except BaseException as e:
            return {'text': 'faild', "data":['前置脚本异常',str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
        #拿取关键字信息
        rekeys = {}
        # if isinstance(bekeys,list):
        #     for i in bekeys:
        #         rekeys[i] = eval(i)
        if httpaction == 'GET':
            print("#"*20,requrl,params,bodys,headers)
            rsp = get(url=requrl,params=params,data=bodys).text
            print(rsp)
        elif httpaction == 'POST':
            try:
                print("#"*50,requrl,params,bodys,headers)
                rsp = post(url=requrl,params=params,data=bodys,headers=headers).text
            except BaseException as e:
                return {'text': 'faild', "data":['接口请求错误',str(e)] }, 202, {"Access-Control-Allow-Origin": "*"}
            rsp = rsp.encode().decode('utf-8')
        elif httpaction == 'HEAD':
            rsp = head(url=requrl,params=params,data=bodys,headers=headers).text
        else :
            return {'text': 'faild', "data": 'HTTP请求方法无效'}, 202, {"Access-Control-Allow-Origin": "*"}
        try:
            exec(assfun)
        except BaseException as e:
            return {'text': 'faild', "data":['断言失败',str(e)]}, 202, {"Access-Control-Allow-Origin": "*"}
        # if isinstance(asskeys,list):
        #     for i in bekeys:
        #         rekeys[i] = eval(i)
        return {'text':'success',"data":[rsp,rekeys]}, 201,{"Access-Control-Allow-Origin": "*"}

class save_apiandcase(Resource):
    def post(self):
        data = request.form.to_dict()
        datadict = change(data)
        api_id,requrl,params,httpaction,headers,bodys,case_id,apicasedetail = datadict["api_id"],datadict["requrl"],datadict["params"],datadict["httpaction"],datadict["headers"],datadict["bodys"],datadict["case_id"],datadict["apicasedetail"]
        befun,assfun = datadict['befun'],datadict['assfun']
        #根据该接口的id更新接口内容
        api_info = Api_info.query.filter(Api_info.id == api_id).first()
        if api_info:
            api_info.httpact = httpaction
            api_info.requrl = requrl
            db.session.add(api_info)
            db.session.commit()
        else:
            base.logger.warning("api_automation.save_apiandcase--api_id error,api_id:{0}".format(api_id))
            return {'text':'api_id undefind'}, 601,{"Access-Control-Allow-Origin": "*"}
        #根据用例的id更新用例内容
        api_case = Apicase_info.query.filter(Apicase_info.id==case_id).first()
        if api_case:
            api_case.params = str(params)
            api_case.bodys = str(bodys)
            api_case.headers = str(headers)
            api_case.apicasedetail = str(apicasedetail)
            api_case.beforefunction = str(befun)
            api_case.assertfunction = str(assfun)
            db.session.add(api_case)
            db.session.commit()
        else:
            base.logger.warning("api_automation.save_apiandcase--case_id error,case_id:{0}".format(case_id))
            return {'text':'case_id undefind'}, 601,{"Access-Control-Allow-Origin": "*"}
        base.logger.info("api_automation.save_apiandcase--save success}")
        return {'text':'success'}, 201,{"Access-Control-Allow-Origin": "*"}

class Get_Api_info(Resource):
    def post(self):
        '''
        方法：post
        路径: /GetApiInfo
        参数：api_id,apicase_id
        业务：api_id所获取的接口id
        apicase_id所获取的用例id
        逻辑：获取接口数据只需要传api_id
        获取用例数据需要传递api_id,apicase_id
        '''
        args = parser.parse_args()
        case_id = args['apicase_id']
        print("1234567890",print(case_id == ''))
        api_id = args["api_id"]
        api_ids = [i.id for i in Api_info.query.all()]
        print('#' * 10, case_id,api_id)
        if case_id is None or case_id == "" and int(api_id) in api_ids:
            #获取接口信息
            api = Api_info.query.filter_by(id=api_id).first()
            api_case = Apicase_info.query.filter_by(api_id=api_id).all()
            case_info = [{'case_id':i.id,'casename':i.casename} for i in api_case]
            print('#'*10,case_info)
            data = {'httpaction':api.httpact,'requrl':api.requrl,'case_id':case_info}
        elif int(api_id) in api_ids:
            #获取用例信息
            print(api_id)
            api_case = Apicase_info.query.filter_by(id=int(case_id)).first()
            data = {'params':api_case.params,'headers':api_case.headers,'body':api_case.bodys,'casename':api_case.casename,'assfun':api_case.assertfunction,'befun':api_case.beforefunction}
        else:
            return {'text':'faild',"data":'输入参数错误'},201,{"Access-Control-Allow-Origin": "*"}
        return {'text':'success',"data":data},201,{"Access-Control-Allow-Origin": "*"}
    pass


class create_apicase(Resource):
    def post(self):
        '''
         方法：post
         路径:/CreateApiCase
         参数：api_id,apicasename
         业务：api_id为添加用例的接口id
         apicasename为添加用例的用例名称
        '''
        args = parser.parse_args()
        casename = args["apicasename"]
        api_id = args["api_id"]
        if casename in ('',None) or api_id in ("",None):
            base.logger.info("api_automation.create_apicase,params error,casename:{0},api_id:{1}".format(casename,api_id))
            return {'text':'必填项不能为空'},601,{"Access-Control-Allow-Origin": "*"}
        #增加apicase_info数据
        base.logger.info("api_automation.create_apicase,Apicase_info insert,casename:{0},api_id:{1}".format(casename,api_id))
        api_case = Apicase_info(api_id=int(api_id),casename=casename)
        db.session.add(api_case)
        db.session.commit()
        case = Apicase_info.query.filter_by(api_id=int(api_id),casename=casename).all()
        #修改api_info的case_id数据
        api = Api_info.query.filter_by(id=int(api_id)).first()
        print(api.case_id)
        if api.case_id == '':
            api.case_id = str(case[-1].id)
        else:
            api.case_id += ',' + str(case[-1].id)
        db.session.add(api)
        db.session.commit()
        #返回caseid
        data = {'apicaseid': case[-1].id}
        base.logger.info("api_automation.create_apicase,create_success,caseid:{0}".format(case[-1].id))
        return {'text':'success',"data":data},201,{"Access-Control-Allow-Origin": "*"}

class Modifi_Api(Resource):
    def post(self):
        '''
            方法：post
            路径： / Modifi_Api
            参数：api_id, api_name, operation
            业务：api_id为修改名称 / 删除的接口id
            api_name为修改名称时的新名称
            operation为‘1’时是修改，为‘2’时是删除
        '''
        #目前只有改变apipath的状态值，重构时需要增加api的状态及用例的状态
        args = parser.parse_args()
        api_tree_id = args["api_tree_id"]
        api_ids = [i.id for i in Fun_path.query.all()]
        if args["operation"] == '1' and int(api_tree_id) in api_ids:
            #修改
            oldapi = Fun_path.query.filter_by(id = api_tree_id).first()
            oldapi.name = args["api_name"]
            db.session.add(oldapi)
            db.session.commit()
        elif args["operation"] == '2' and int(api_tree_id) in api_ids:
            #删除
            oldapi = Fun_path.query.filter_by(id=api_tree_id).first()
            oldapi.classify = '3'
            db.session.add(oldapi)
            db.session.commit()
        else:
            return {'text': 'faild', "data": "输入的参数错误"}, 201, {"Access-Control-Allow-Origin": "*"}
        return {'text':'success',"data":"操作成功"}, 201,{"Access-Control-Allow-Origin": "*"}




