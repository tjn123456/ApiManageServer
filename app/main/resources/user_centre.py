# -*- coding: utf-8 -*-
'''
用户中心 页面接口

'''
from flask_restful import reqparse,Resource
from ..basic import base
from ..basic import beehive_redis
from ...models import User

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class User_message(Resource):
    def get(self):
        #获取用户信息
        pass

    def post(self):
        #注册
        pass


class User_login(Resource):
    def post(self):
        #登录
        args = parser.parse_args()
        username = args['username']
        passwd = base.getmd5(args['password'])
        base.logger.info("user_centre.User_login--user:{0},password:{1}".format(username,args['password']))
        token = base.encrypt(username+','+passwd)
        #token 为byte值时无法以json传递至客户端
        token = token.decode()
        savetoken = beehive_redis.settoken(username,token)
        user = User.query.filter(User.username==username, User.password==passwd).first()
        if user:
            icon = user.icon_url
            base.logger.info("user_centre.User_login--login success,user:{0},token:{1},icon:{2}".format(username,token,icon))
            return {'text':'登录成功','status':'1','data':{'username':username,'token':token,'usericon':icon}},201,{"Access-Control-Allow-Origin": "*"}
        else:
            base.logger.warning("user_centre.User_login--login faild,user:{0},token:{1}".format(username,token))
            return {'text':'账号密码错误','status':'0'}, 602,{"Access-Control-Allow-Origin": "*"}

