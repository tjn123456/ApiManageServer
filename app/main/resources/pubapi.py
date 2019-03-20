# -*- coding: utf-8 -*-
"""
    Main_Path 是主目录的函数（只有查询功能），从Main_path的表中取值
    Fun_Path 是各功能目录的函数（拥有增删改查功能），从Fun_path的表中取值

"""

import sys
from flask_restful import reqparse,Resource,request
from ...model_path import Main_path,Fun_path
from ...models2 import Api_info
sys.path.append("....")
from app import db

parser = reqparse.RequestParser()
parser.add_argument('api_tree_id',type=str)
parser.add_argument('apifa_id',type=str)
parser.add_argument('api_name',type=str)
parser.add_argument('add_type',type=str)




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
        '''menu为接口目录，parent为所有目录对象（用于前端关联父级目录使用）'''
        data = Fun_path.query.filter_by(classify=1).all()
        list = [{'id': str(i.id), 'text': i.name, 'value': i.fun_id, 'pid': i.fa_id} for i in data]
        # 将所有的子目录格式改为{pid:{obj}}
        id = [str(i.id) for i in data]
        di = {}
        for i in id:
            re = []
            for j in list:
                if j['pid'] == i:
                    re.append(j)
            if re != []:
                di[i] = re

        # 将子目录放入腹肌目录内
        for i in list:
            for j in di.keys():
                if i['id'] == j:
                    i['item'] = di[j]

        # 将重复的子目录清除
        list = [i for i in list if i['pid'] == '']

        parent_obj = Fun_path.query.filter(Fun_path.fun_id == '' ).all()
        parent = [{'id': str(i.id), 'text': i.name,} for i in parent_obj]
        result = {}
        result["menu"] = list
        result["parent"] = parent
        return {'text':'success',"data":result}, 201,{"Access-Control-Allow-Origin": "*"}

    def post(self):
        """增加或修改目录"""
        args = parser.parse_args()
        fa_id = args["apifa_id"] if args["apifa_id"] else ''
        api_tree_id = args["api_tree_id"] if args["api_tree_id"] else ''
        api_name = args["api_name"] if args["api_name"] else ''
        #type 1 是目录，2是接口
        type = args["add_type"]
        api_ids = [i.id for i in Fun_path.query.all()]
        if api_tree_id =='':
            if type == '1':
                #增加目录
                addpath = Fun_path(classify="1",name=api_name,fa_id=fa_id,fun_id='')
                db.session.add(addpath)
                db.session.commit()
            elif type =='2':
                #增加接口
                # 增加空的接口信息获取fun_id
                addapiinfo = Api_info(apiname=api_name, apidetail='', httpact='', requrl='', case_id='')
                db.session.add(addapiinfo)
                db.session.commit()
                #增加子目录
                addpath = Fun_path(fun_id=addapiinfo.id,fa_id=fa_id,classify="1",name=api_name)
                db.session.add(addpath)
                db.session.commit()
        elif int(api_tree_id) in api_ids:
            # 修改
            oldname = Fun_path.query.filter_by(id=api_tree_id).first()
            oldname.name = api_name
            db.session.add(oldname)
            db.session.commit()
        else:
            return {'text':'faild',"data":"输入的参数错误"}, 601,{"Access-Control-Allow-Origin": "*"}
        return {'text':'success',"data":"目录添加成功"}, 201,{"Access-Control-Allow-Origin": "*"}

