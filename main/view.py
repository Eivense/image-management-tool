import json
from flask import jsonify,make_response
from . import app
from .Celery.celery_tasks import rsync
from .Connection.redis_conn import Redis
from .Celery.Workers import Workers
from .config import json_path
from ..main.Util import Util
from datetime import datetime,timedelta

@app.route('/')
def hello_world():
    return "hello world"


@app.route('/rsync')
def flask_rsync():
    list=['elvish','inna','putty','vim']
    result=[]
    for i in list:
        task=rsync.apply_async(args=[i])
        result.append(task.id)
    return jsonify(result)

@app.route('/redis')
def get_queue():
    conn=Redis.connect()
    keys=Redis.get_all(conn)
    queue=[]
    for key in keys:
        value=Redis.get(conn,key)
        b=json.loads(bytes.decode(value))
        queue.append(b)
    return jsonify(queue)

@app.route('/task_status')
def get_task():
    json=Util.read_json(json_path)
    response = make_response(jsonify(json))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/kill')
def kill_all():
    workers=Workers.getWorkers()
    workers.kill()
    return "success"


@app.route('/stop')
def stop_all():
    workers=Workers.getWorkers()
    workers.stopAll()
    return "success"

@app.route('/createworker/<worker_name>')
def createworker(worker_name):
    workers=Workers.getWorkers()
    workers.createNewWorker(worker_name)
    return "success"