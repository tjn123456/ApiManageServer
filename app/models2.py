# -*- coding: utf-8 -*-
from . import db
from datetime import datetime

class Api_info(db.Model):
    '''
        接口信息表
        id 接口编号，自增，主键
        apiname 接口名
        apidetail 接口详情
        httpact http请求方法
        requrl 请求地址
        case_id 关联的测试用例需用增量修改
    '''
    __tablename__ = 'api_info'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    apidetail = db.Column(db.String(256))
    httpact = db.Column(db.String(64))
    requrl = db.Column(db.String(128))
    case_id = db.Column(db.String(256))
    status = db.Column(db.String(8))

    def __init__(self,apiname='',apidetail='',httpact='',requrl='',case_id='',status=''):
        self.name = apiname
        self.apidetail = apidetail
        self.httpact = httpact
        self.requrl = requrl
        self.case_id = case_id
        self.status = status

    def __repr__(self):
         return '<Api_info %r>' % self.name

class Apicase_info(db.Model):
    '''
        接口用例信息表
        id 接口用例编号，自增，主键
        casename 用例名称
        api_id 接口编号
        params url后缀参数
        headers 请求头部信息参数
        bodys 请求体信息参数
        apicasedetail 接口用例详情
        beforefunction 前置脚本
        assertfunction  断言脚本
    '''
    __tablename__ = 'apicase_info'
    id = db.Column(db.Integer,primary_key=True)
    casename = db.Column(db.String(128))
    api_id = db.Column(db.Integer)
    params = db.Column(db.String(256))
    headers = db.Column(db.String(256))
    bodys = db.Column(db.String(256))
    apicasedetail = db.Column(db.String(256))
    beforefunction = db.Column(db.String(1024))
    assertfunction = db.Column(db.String(1024))

    def __init__(self,api_id='',params='',headers='',bodys='',apicasedetail='',casename='',beforefunction='',assertfunction=''):
        self.casename = casename
        self.api_id = api_id
        self.params = params
        self.headers = headers
        self.bodys = bodys
        self.apicasedetail = apicasedetail
        self.beforefunction = beforefunction
        self.assertfunction = assertfunction


    def __repr__(self):
         return '<Apicase_info %r>' % self.id

class Project_task(db.Model):
    '''
        任务项目表
        name 任务名称，自增，主键
        count_log 任务执行信息，内容为执行成功数量，失败数量，阻塞数量，总数，执行日志{'success':'','block':'','faild':'','total':'',log:{'log':'status'}}
        testcase 用例集ID
        detail 任务描述
        createtime 创建时间
        updatetime 修改时间
        status 状态1为待执行/完成执行，2为执行中，
    '''
    __tablename__ = 'project_task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    count_log = db.Column(db.Text)
    testcase = db.Column(db.String(256))
    detail = db.Column(db.String(128))
    createtime = db.Column(db.DateTime,default=datetime.now())
    updatetime = db.Column(db.DateTime,default=datetime.now())
    status = db.Column(db.String(32))


    def __init__(self,name='', count_log='', testcase='', detail='', status=''):
        self.name = name
        self.count_log = count_log
        self.testcase = testcase
        self.detail = detail
        self.status = status
    def __repr__(self):
        return '<Project_task %r>' % self.id