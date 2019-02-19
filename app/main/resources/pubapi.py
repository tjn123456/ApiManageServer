# -*- coding: utf-8 -*-
"""
    Main_Path 是主目录的函数（只有查询功能），从Main_path的表中取值
    Fun_Path 是各功能目录的函数（拥有增删改查功能），从Fun_path的表中取值

"""

import sys
from flask_restful import reqparse,Resource,request
from ..basic.base import get_fun_path
from ...model_path import Main_path,Fun_path
from ...models2 import Api_info
sys.path.append("....")
from app import db

parser = reqparse.RequestParser()
parser.add_argument('api_tree_id',type=str)
parser.add_argument('apifa_id',type=str)
parser.add_argument('api_name',type=str)



class Main_Path(Resource):
    def get(self):
        data = Main_path.query.all()
        if data in ["",None]:
            return {'text': 'Main_path is none'}, 601, {"Access-Control-Allow-Origin": "*"}
        list = []
        son = {}
        for i in data:
            dict = {'id': i.id, 'text': i.pathname, 'value': i.main_url, 'item': ''}
            if i.fa_id:
                dict2 = {'id': i.id, 'text': i.pathname, 'value': i.main_url}
                if i.fa_id not in son.keys():
                    son[i.fa_id] = []
                son[i.fa_id].append(dict2)
            else:
                list.append(dict)
        for i in son.keys():
            for a in list:
                if i == a['id']:
                    a['item'] = son[i]
        result = {}
        result["row"] = list
        return {'text':'success',"data":result}, 201,{"Access-Control-Allow-Origin": "*"}

class Api_Path(Resource):
    def get(self):
        result = get_fun_path('1',Api_info)
        return {'text':'success',"data":result}, 201,{"Access-Control-Allow-Origin": "*"}

    def post(self):
        """增加或修改目录"""
        args = parser.parse_args()
        fa_id = args["apifa_id"]
        api_tree_id = args["api_tree_id"]
        api_name = args["api_name"]
        print("###############################################")
        print(fa_id,api_tree_id,api_name)
        print(type(fa_id))
        api_ids = [i.id for i in Fun_path.query.all()]
        fa_ids = [i.fa_id for i in Fun_path.query.all()]
        print(api_ids)
        if int(api_tree_id) in api_ids:
            #修改
            oldname = Fun_path.query.filter_by(id = api_tree_id).first()
            oldname.name = api_name
            db.session.add(oldname)
            db.session.commit()
        elif fa_id == '0':
            #增加父目录
            addpath = Fun_path(classify="1",name=api_name,fa_id='',fun_id='')
            db.session.add(addpath)
            db.session.commit()
        elif int(fa_id) in api_ids:
            #增加空的接口信息获取fun_id
            addapiinfo = Api_info(apiname='',apidetail='',httpact='',requrl='',case_id='')
            db.session.add(addapiinfo)
            db.session.commit()
            #增加子目录
            addpath = Fun_path(fun_id=addapiinfo.id,fa_id=fa_id,classify="1",name=api_name)
            db.session.add(addpath)
            db.session.commit()
        else:
            return {'text':'faild',"data":"输入的参数错误"}, 601,{"Access-Control-Allow-Origin": "*"}
        return {'text':'success',"data":"目录添加成功"}, 201,{"Access-Control-Allow-Origin": "*"}

