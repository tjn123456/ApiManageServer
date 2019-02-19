# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import reqparse,Resource,request,Api
import sys
import random
import time
from redis import Redis
from rq import Queue

sys.path.append("..")
from test_app import user_valid

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


app = Flask(__name__)
app.config["CELERY_BROKER_URL"]='redis://127.0.0.1:6379/1'
app.config['result_backend']='redis://127.0.0.1:6379/3'
api = Api(app)
print(app.name)




def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = 100
    print(123)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i,'total': total,'status': message})
        print(message)
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

q = Queue(connection=Redis())
def abc(a):
    for i in range(10):
        print(i)
        time.sleep(1)
    return a

class todo(Resource):
    def get(self):
        job = q.enqueue(abc,'dd')
        return {'text': 'success'}, 201, {"Access-Control-Allow-Origin": "*"}


api.add_resource(todo,'/task')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)

