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