# -*- coding: utf-8 -*-
'''
代替python rq功能中的worker工作
启动方式 python dxcworker.py
'''
import os
import logging
import sys
import signal
import redis
import multiprocessing
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
redis_url = 'redis://localhost:6379'
conn = redis.from_url(redis_url)
def sigint_handler(signum, frame):
    for i in pid_list:
        os.kill(i, signal.SIGKILL)
    logging.info("exit...")
    sys.exit()
def worker():
    logging.info('this is worker')
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
pid_list = []
signal.signal(signal.SIGINT, sigint_handler)
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)  # multiprocessing pool多进程池，processes=4 指定进程数
    for i in range(3):
        pool.apply_async(worker, )
    for i in multiprocessing.active_children():
        pid_list.append(i.pid)
    pid_list.append(os.getpid())
    pool.close()
    pool.join()