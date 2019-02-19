# -*- coding: utf-8 -*-
'''
    路由文件
'''
from .main.resources.monkey import Monpush
from .main.resources.user_centre import User_login
from .main.resources.api_automation import api_single,create_apicase,save_apiandcase,Modifi_Api,Get_Api_info
from .main.resources.pubapi import Main_Path,Api_Path
from .main.resources.tasks import Api_Task,Api_Runtask




def add_route(api):
    api.add_resource(Monpush,'/apply')
    api.add_resource(User_login,'/login')
    api.add_resource(api_single,'/apisingle')
    api.add_resource(create_apicase,'/CreateApiCase')
    api.add_resource(save_apiandcase, '/SaveApiAndCase')
    api.add_resource(Main_Path,'/MainPath')
    api.add_resource(Api_Path, '/ApiPath')
    api.add_resource(Modifi_Api,'/ModifiApi')
    api.add_resource(Get_Api_info,'/GetApiInfo')
    api.add_resource(Api_Task,'/ApiTaskInfo')
    api.add_resource(Api_Runtask,'/ApiRunTask')
