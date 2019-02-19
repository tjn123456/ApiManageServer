# -*- coding: utf-8 -*-
'''
    程序配置文件
    选择不同的环境参数指定不同的数据库
'''

import os
import logging

#获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

#Development的数据库连接路径
deveuri = 'mysql+pymysql://root:123456@47.105.82.150:3306/beehive?charset=utf8'
#redis数据库路径会被程序内basic库中redis引用
redis_url = {'url':'127.0.0.1','port':'6379'}
#日志配置
log_config = {"logger":logging.getLogger('flask_log'),
              'all_log_level':logging.DEBUG,
              'error_log_level':logging.ERROR,
              'all_log_path':"log/all.log",
              "error_log_path":"log/error.log"}

#Flask-SQLAlchemy执行完逻辑之后自动提交,不需要手动commit
class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

'''
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
'''



#开发环境
class DevelopmentConfig(Config):
    #debug模式可以在修改代码后，服务自动重启加载
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = deveuri
    STORAGE_URL = redis_url
    # CELERY_BROKER_URL ='redis://127.0.0.1:6379/1'
    # result_backend = 'redis://127.0.0.1:6379/3'



#测试环境--几乎用不上
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

#生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
