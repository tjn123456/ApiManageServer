# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import reqparse,Resource,request,Api
from flask_sqlalchemy import SQLAlchemy
# 配置数据库连接
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://root:123456@localhost:3306/beehive?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)

# 创建用户角色表
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=True)
    # 定义一对多关联关系
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
# 创建用户表
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.String(11), primary_key=True)
    uname = db.Column(db.String(11), unique=True, nullable=True)
    pwd = db.Column(db.String(11), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    regtime = db.Column(db.String(20), nullable=True)
    stat = db.Column(db.String(1), nullable=True)
    # 定义外键
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User %r>' % self.uname


if __name__ == '__main__':
    print(db)
    app.run(host="0.0.0.0",port=5000,debug=True)
