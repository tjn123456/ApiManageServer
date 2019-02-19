# -*- coding: utf-8 -*-
from . import db

class Main_path(db.Model):
    '''
        主业务目录
        id 目录编号，自增，主键
        pathname 目录名称，128位字符
        fa_id 父级目录id，
        main_url 目录链接
    '''
    __tablename__ = 'main_paths'
    id = db.Column(db.Integer,primary_key=True)
    pathname = db.Column(db.String(128))
    fa_id = db.Column(db.Integer)
    main_url = db.Column(db.String(128))


    def __init__(self,name,fa_id,main_url):
        self.pathname = name
        self.fa_id = fa_id
        self.main_url = main_url


    def __repr__(self):
        return '<Main_path %r>' % self.pathname

class Fun_path(db.Model):
    '''
     主业务目录
     id 目录编号，自增，主键
     fa_id 父级目录id，
     fun_id 关联api或UI的数据id
     classify 1标识为api,2标识为UI
    '''
    __tablename__ = 'fun_paths'
    id = db.Column(db.Integer,primary_key=True)
    fa_id = db.Column(db.String(16))
    fun_id = db.Column(db.String(128))
    classify = db.Column(db.String(128))
    name = db.Column(db.String(128))

    def __init__(self,fa_id,fun_id,classify,name):
        self.fa_id = fa_id
        self.fun_id = fun_id
        self.classify = classify
        self.name = name


    def __repr__(self):
        return '<Fun_path %r>' % self.name

    # def init_table(self):
    #     db.session.execute('ALTER TABLE users AUTO_INCREMENT = 2000;')