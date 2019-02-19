# -*- coding: utf-8 -*-
'''
    该文件为基础函数
    getmd5将数据加密为md5并返回
    encrypt将字符串加密为token
    decrypt将token解密为字符串
    get_fun_path将数据库输入数据库对象返回目录列表数据(接口测试和UI测试的目录)
'''
import hashlib
import sys
import base64
from ...model_path import Fun_path
import logging
import logging.handlers
import datetime
sys.path.append("....")
from config import log_config


def getmd5(passwd):
    h = hashlib.md5()
    h.update(passwd.encode(encoding='utf-8'))
    md5val = h.hexdigest()
    return md5val

def encrypt(token_str):
    token_str = token_str.encode(encoding="utf-8")
    token = base64.b64encode(token_str)
    return token

def decrypt(token):
    token_str = base64.b64decode(token)
    return token_str.decode()

def get_fun_path(classify,dbobj):
    """此函数复用时需注意数据表对应的字段名称统一"""
    data = Fun_path.query.filter_by(classify=classify).all()
    list = []
    son = {}
    for i in data:
        dict = {'id': i.id, 'text': i.name, 'value': i.fun_id, 'item': ''}
        if i.fa_id:
            dict2 = {'id': i.id, 'text': i.name, 'value': i.fun_id}
            if i.fa_id not in son.keys():
                son[i.fa_id] = []
            son[i.fa_id].append(dict2)
        else:
            list.append(dict)
    #print('*' * 30, son, list)
    for i in son.keys():
        for a in list:
            if i == str(a['id']):
                a['item'] = son[i]
    result = {}
    result["row"] = list
    return result

def logger_init():
    logger = log_config["logger"]
    logger.setLevel(log_config["all_log_level"])

    rf_handler = logging.handlers.TimedRotatingFileHandler(log_config["all_log_path"], when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler(log_config["error_log_path"])
    f_handler.setLevel(log_config["error_log_level"])
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger
logger = logger_init()