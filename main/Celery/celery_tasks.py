import os
import time

from ..config import json_path,rsync_path
from .. import celery
from ..Util import Util
from ..Celery import BaseTask

@celery.task(name='rsync',bind=True,base=BaseTask)
def rsync(self,name):
    task_id=self.request.id
    hostname=self.request.hostname
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mirrors=Util.read_json(json_path)
    if("end_time" in mirrors[name]):
        last_succeed=mirrors[name]["end_time"]
    else:
        last_succeed=""
    task={
        "task_id":task_id,
        "start_time":start_time,
        "hostname":hostname,
        "status":"STARTED",
        "last_succeed":last_succeed,
        "end_time":"",
        "message":"",
    }
    Util.save_object(task,name,json_path)
    time.sleep(30)
    rsync=os.system(rsync_path+" "+name)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if (rsync == 0):
        last_succeed = end_time
        status="SUCCEEDED"
    else:
        status="RSYNC_FAILED"
    task["end_time"]=end_time
    task["last_succeed"]=last_succeed
    task["status"]=status
    task["message"]=Util.rsync_exitcode(rsync>>8)
    Util.save_object(task,name,json_path)
    return rsync>>8