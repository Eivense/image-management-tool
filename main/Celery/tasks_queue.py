import os
import time

from pj.main.Connection.mongo_conn import MongoDB
from ..Model.Task import Task
from .. import celery
from ..Util import JsonUtil

@celery.task(name='rsync',bind=True)
def rsync(self,name):
    task_id=self.request.id
    image=JsonUtil.read_json_toObject(name)
    print(type(image))
    starttime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    image.status="Syncing"
    JsonUtil.save_object(image.tojson())
    task=Task(task_id, name, starttime, self.request.hostname)
    connection=MongoDB.connect()
    MongoDB.insert(connection,task.convert_to_dict())
    rsync=os.system('/home/eivense/sync_script/rsync.sh '+name)
    endtime=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    MongoDB.update(connection,task_id,endtime)
    return rsync>>8