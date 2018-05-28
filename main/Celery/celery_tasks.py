import os
import time

from ..config import mirror_path,rsync_path,file_path,shell_path
from .. import celery,mirrors
from ..Util import Util
from .BaseTask import BaseTask
from ..Model.Task import Task
from ..Model.Mirror import Mirror
@celery.task(name='rsync',bind=True,base=BaseTask,timelimit=20)
def rsync(self,name,upstream):
    task_id=self.request.id
    hostname=self.request.hostname
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mirrors=Util.read_json(mirror_path)
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
    Util.save_object(task,name,mirror_path)
    time.sleep(30)
    rsync=os.system(rsync_path+" "+name+" "+upstream+" "+file_path)
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
    Util.save_object(task,name,mirror_path)
    return rsync>>8



@celery.task(name='test',bind=True,base=BaseTask)
def test(self,name,upstream):
    task_id = self.request.id
    hostname = self.request.hostname
    start_time =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    mirror=Mirror(name=name,task_id=task_id,hostname=hostname,start_time=start_time,status="STARTED")
    task=Task(name=name,task_id=task_id,hostname=hostname,status="STARTED",start_time=start_time)
    data=mirrors.find_one({"_id":self.name})
    if(data):
        mirror.lastsucceed=data['last_succeed']
    else:
        mirror.lastsucceed=""
    mirror.save()
    task.save()
    time.sleep(30)
    if(os.path.isfile(os.path.join(shell_path,name+".sh"))):
        rsync=os.system(shell_path+name+".sh"+" "+name+" "+upstream+" "+file_path)
    else:
        rsync = os.system(rsync_path + " " + name + " " + upstream + " " + file_path)
    end_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if (rsync>>8 == 0):
        mirror.lastsucceed = end_time
        status="SUCCEEDED"
    else:
        status="RSYNC_FAILED"
    mirror.status=status
    mirror.end_time=end_time
    mirror.message=Util.rsync_exitcode(rsync>>8)
    mirror.update()
    return rsync>>8

