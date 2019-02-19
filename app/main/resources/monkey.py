# -*- coding: utf-8 -*-
'''
monkey 页面接口
Monpush：
        1、判断参数有效性
        2、向deadpool传递脚本命令
'''
from flask import request
from flask_restful import reqparse,Resource
import requests
from ..resources import user_valid
from ..basic import base



parser = reqparse.RequestParser()
parser.add_argument('package_name', type=str)
parser.add_argument('click_count', type=str)


class Monpush(Resource):
    def post(self):
        if user_valid():
            ip = request.remote_addr
            url = 'http://'+ip+':9999/mon'
            print(url)
            args = parser.parse_args()
            if args['package_name'] in ['',None] or args['click_count'] in ['',None]:
                base.logger.warning("monkey.Monpush--params error,package:{0},click_count:{1}".format(args['package_name'],args['click_count']))
                return {'text':'请填写正确的包名与点击次数'}, 601, {"Access-Control-Allow-Origin": "*"}
            data = {'monscript':'adb shell monkey -p ' + args['package_name'] +  ' --throttle 100  --monitor-native-crashes -v -v  -s 10 '+ args['click_count'],
                    'closcript':'adb shell am force-stop '+ args['package_name'],}
            base.logger.info("monkey.Monpush--adb shell:{monscript},closecript:{closcript}".format(**data))
            res = requests.post(url,data)
            result = res.text
            print(result)
            base.logger.info("monkey.Monpush--test_success,result:{0}".format(result))
            return {'text':'请求成功',"data":result}, 201,{"Access-Control-Allow-Origin": "*"}
        else:
            base.logger.warning("monkey.Monpush--token error")
            return {'text': 'token无效'},609,{"Access-Control-Allow-Origin": "*"}






