# -*- coding: utf-8 -*-
'''
    数据库模型文件
'''
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app
# from flask_login import UserMixin, AnonymousUserMixin
from . import db
from datetime import datetime


class User(db.Model):
    '''
        用户信息表
        id 用户编号，自增，主键
        username 用户名，64位字符，非空
        password 密码，64位字符，非空
        status 状态，1使用中，2为失效----功能未实现
        roleid 权限关联
        createtime 创建时间，为当前时间
        icon_url 用户头像地址，目前存放在img中
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))
    status = db.Column(db.Integer,default=1)
    roleid = db.Column(db.Integer)
    createtime = db.Column(db.DateTime,default=datetime.now())
    icon_url = db.Column(db.String(128))

    def __init__(self,name,password,status,roleid,icon_url):
        self.username = name
        self.password = password
        self.status = status
        self.roleid = roleid
        self.icon_url = icon_url

    def __repr__(self):
         return '<User %r>' % self.username

    # def init_table(self):
    #     db.session.execute('ALTER TABLE users AUTO_INCREMENT = 2000;')

class Role(db.Model):
    '''
        用户权限表
        id 权限编号，主键，自增
        rolename 职务名称，64位字符，非空
        permissions 权限等级，1为admin，2为tester，3为dev ----功能未实现
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    rolename = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)

    def __init__(self, name, permissions):
        self.rolename = name
        self.permissions = permissions


    def __repr__(self):
        return '<Role %r>' % self.rolename

# class Main_path(db.Model):
#     '''
#         主业务目录
#         id 目录编号，自增，主键
#         pathname 目录名称，128位字符
#         fa_id 父级目录id，
#         main_url 目录链接
#     '''
#     __tablename__ = 'main_paths'
#     id = db.Column(db.Integer, primary_key=True)
#     pathname = db.Column(db.String(128))
#     fa_id = db.Column(db.Integer)
#     main_url = db.Column(db.String(128))
#
#     def __init__(self, name, fa_id, main_url):
#         self.pathname = name
#         self.fa_id = fa_id
#         self.main_url = main_url
#
#     def __repr__(self):
#         return '<User %r>' % self.pathname

    # def init_table(self):
    #     db.session.execute('ALTER TABLE roles AUTO_INCREMENT = 6000;')



# class Permission:
#     FOLLOW = 0x01
#     COMMENT = 0x02
#     WRITE_ARTICLES = 0x04
#     MODERATE_COMMENTS = 0x08
#     ADMINISTER = 0x80
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User': (Permission.FOLLOW |
#                      Permission.COMMENT |
#                      Permission.WRITE_ARTICLES, True),
#             'Moderator': (Permission.FOLLOW |
#                           Permission.COMMENT |
#                           Permission.WRITE_ARTICLES |
#                           Permission.MODERATE_COMMENTS, False),
#             'Administrator': (0xff, False)
#         }
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.permissions = roles[r][0]
#             role.default = roles[r][1]
#             db.session.add(role)
#         db.session.commit()
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#     password_hash = db.Column(db.String(128))
#     confirmed = db.Column(db.Boolean, default=False)
#
#     def __init__(self, **kwargs):
#         super(User, self).__init__(**kwargs)
#         if self.role is None:
#             if self.email == current_app.config['FLASKY_ADMIN']:
#                 self.role = Role.query.filter_by(permissions=0xff).first()
#             if self.role is None:
#                 self.role = Role.query.filter_by(default=True).first()
#
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#     def generate_confirmation_token(self, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'confirm': self.id})
#
#     def confirm(self, token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('confirm') != self.id:
#             return False
#         self.confirmed = True
#         db.session.add(self)
#         return True
#
#     def generate_reset_token(self, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'reset': self.id})
#
#     def reset_password(self, token, new_password):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('reset') != self.id:
#             return False
#         self.password = new_password
#         db.session.add(self)
#         return True
#
#     def generate_email_change_token(self, new_email, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'change_email': self.id, 'new_email': new_email})
#
#     def change_email(self, token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('change_email') != self.id:
#             return False
#         new_email = data.get('new_email')
#         if new_email is None:
#             return False
#         if self.query.filter_by(email=new_email).first() is not None:
#             return False
#         self.email = new_email
#         db.session.add(self)
#         return True
#
#     def can(self, permissions):
#         return self.role is not None and \
#             (self.role.permissions & permissions) == permissions
#
#     def is_administrator(self):
#         return self.can(Permission.ADMINISTER)
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#
# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False
#
#     def is_administrator(self):
#         return False
#
# login_manager.anonymous_user = AnonymousUser
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
