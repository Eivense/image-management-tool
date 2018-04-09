from __future__ import absolute_import
import time
import json
from pj.main.Util import Util
from pj.main import celery


def monitor(celery):
    state = celery.events.State()
    result = {}
    def task_received(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_id = task.uuid
        task_name = task.args
        received_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.received))
        image={
            "received_time":received_time,
            "task_id":task_id
        }
        result[task_name]=image
        print(result)

    def task_started(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        task_name=task.args
        started_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.started))
        result[task_name]["started_time"] = started_time
        print(result)

    with celery.connection() as connection:
        recv = celery.events.Receiver(connection, handlers={
            'task-received': task_received,
            'task-started': task_started,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


monitor(celery)