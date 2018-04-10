import os
import time

from ..config import json_path,rsync_path
from ..Model.Task import Task
from .. import celery
from ..Util import Util
from ..Celery import BaseTask


@celery.task(name='rsync',bind=True,base=BaseTask)
def rsync(self,name):
    task_id=self.request.id
    hostname=self.request.hostname
    #starttime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    task=Task(name,task_id,hostname=hostname)
    Util.save_object(task,json_path)
    rsync=os.system(rsync_path+" "+name)
    #endtime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    #task.endtime=endtime
    #task.status=self.AsyncResult(task_id).state
    task.exitcode_message=Util.rsync_exitcode(rsync>>8)
    Util.save_object(task, json_path)
    return rsync>>8