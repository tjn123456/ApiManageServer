# -*- coding: utf-8 -*-
'''
    主程序配置文件
    主程序操作内容见readme

'''
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from app.model_path import Main_path
from app.models2 import Api_info, Apicase_info
from flask_script import Manager, Shell, Server, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app.route import add_route
from app.main.basic.base import getmd5




#获取一个名为flask_config的环境变量为config的启动项'development': DevelopmentConfig,'testing': TestingConfig,'production': ProductionConfig,'default': DevelopmentConfig
app,api= create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
add_router = add_route(api)



#在shell模式下预加载对象（如数据库对象db，应用程序对象app，表对象等）
def make_shell_context():
    return dict(app=app, db=db,user=User,role=Role,api=api,main_path=Main_path)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver',Server(host="0.0.0.0", port=5001,threaded=True))

#创建shell模式下的快捷方法--创建数据表
@manager.command
def create():
    db.create_all()
    return '数据库已创建'

#创建shell模式下的快捷方法--删除数据表
@manager.command
def drop():
    if prompt_bool('确定要删除数据库然后跑路吗？'):
        db.drop_all()
        return '数据库删除完成'
    return '删除需谨慎！'

#创建shell模式下的快捷方法--注册用户
@manager.command
def sign_in():
    print("请输入登录名")
    username = input()
    print('请输入密码')
    password = input()
    password = getmd5(password)
    icon_list = ['d1.png', 'd10.png', 'd11.png', 'd13.png', 'd15.png', 'd16.png', 'd2.png', 'd6.png', 'd7.png',
                 'd9.png']
    print('请输入头像编号0:超人，1:美国队长，2:闪电侠，3:死侍，4:蜘蛛侠，5:蝙蝠侠，6:钢铁侠，7:雷神，8:杰尼龟，9:绿巨人')
    icon = input()
    icon = int(icon)
    usericon = '../static/img/' + icon_list[icon]
    #status = 1 为有效用户
    status = 1
    #roleid = 2 为测试工程师
    roleid = 2
    add_user = User(username,password,status,roleid,usericon)
    db.session.add(add_user)
    db.session.commit()
    return "success"




if __name__ == '__main__':
    manager.run()






















