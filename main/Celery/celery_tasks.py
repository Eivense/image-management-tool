import os
import time

from ..config import json_path,rsync_path
from ..Model.Task import Task
from .. import celery
from ..Util import Util

@celery.task(name='rsync',bind=True)
def rsync(self,name):

    task_id=self.request.id
    hostname=self.request.hostname
    starttime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    task=Task(name,task_id,"Syncing",starttime,hostname)
    Util.save_object(task,json_path)
    rsync=os.system(rsync_path+" "+name)
    endtime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    task.endtime=endtime
    if(rsync==0):
        task.status="Success"
    else:
        task.status="Error"
    task.exitcode_message=Util.rsync_exitcode(rsync>>8)
    Util.save_object(task, json_path)
    return rsync>>8