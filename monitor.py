from __future__ import absolute_import
import time
import json
from pj.main.Util import Util
from pj.main import celery
from pj.main.config import json_path
def monitor(celery):
    state = celery.events.State()
    def task_received(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_name = task.args
        task_name = task_name[2:]
        task_name = task_name[:-2]
        result = Util.read_json(json_path)
        result[task_name]["status"] = task.state
        Util.save_json_tofile(result, json_path)

    def task_started(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_name=task.args
        task_name=task_name[2:]
        task_name=task_name[:-2]
        started_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.started))
        result=Util.read_json(json_path)
        result[task_name]["start_time"] = started_time
        result[task_name]["status"]=task.state
        Util.save_json_tofile(result,json_path)

    def task_succeeded(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_name=task.args
        task_name=task_name[2:]
        task_name=task_name[:-2]
        succeeded_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.succeeded))
        result=Util.read_json(json_path)
        result[task_name]["end_time"] = succeeded_time
        result[task_name]["status"]=task.state
        Util.save_json_tofile(result,json_path)

    def task_failed(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_name=task.args
        task_name=task_name[2:]
        task_name=task_name[:-2]
        failed_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.failed))
        result=Util.read_json(json_path)
        result[task_name]["end_time"] = failed_time
        result[task_name]["status"]=task.state
        result[task_name]["message"]
        Util.save_json_tofile(result,json_path)

    with celery.connection() as connection:
        recv = celery.events.Receiver(connection, handlers={
            'task-received': task_received,
            'task-started': task_started,
            'task-succeeded':task_succeeded,
            'task-failed':task_failed,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


monitor(celery)