# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from config import config

'''
    app默认加载内容
    create_app，初始化APP并加载配置文件内容
'''

db = SQLAlchemy()



def create_app(config_name):
    '''
    app初始化创建APP
    导入配置文件
    增加接口路由
    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    api = Api(app)


    return app,api
	



