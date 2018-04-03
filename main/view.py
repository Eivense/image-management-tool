import json

from flask import jsonify

from . import app
from .Celery.tasks_queue import *
from .Connection.redis_conn import Redis


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/rsync')
def flask_rsync():
    #list=['elvish','inna','putty','vim']
    list=['elvish']
    result=[]
    for i in list:
        task=rsync.apply_async(args=[i])
        result.append(task.id)
    return jsonify(result)

@app.route('/queue')
def get_queue():
    conn=Redis.connect()
    keys=Redis.get_all(conn)
    queue=[]
    for key in keys:
        value=Redis.get(conn,key)
        b=json.loads(bytes.decode(value))
        queue.append(b)
    return jsonify(queue)

@app.route('/task')
def get_task():
    connection=MongoDB.connect()
    result=MongoDB.find_all(connection)
    print(type(result))
    return jsonify(result)


@app.route('/status')
def task_status():
    return 1