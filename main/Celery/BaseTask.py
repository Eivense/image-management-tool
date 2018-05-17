import celery
import datetime
import time
from .. import tasks,mirrors
from ..Model.Task import Task
from ..Model.Mirror import Mirror
from ..Util.Util import rsync_exitcode
class BaseTask(celery.Task):
    abstract = True
    def on_success(self, retval, task_id, args, kwargs):
        task_name=args[0]
        task=tasks.find_one({"_id":task_id})
        end_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if(retval==0):
            status="SUCCEEDED"
        else:
            status="RSYNC_FAILED"
        runtime=datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(task["start_time"],"%Y-%m-%d %H:%M:%S")
        data=Task(task_id=task_id,name=task_name,status=status,start_time=task["start_time"],
                  end_time=end_time,hostname=task["hostname"],message=rsync_exitcode(retval),runtime=runtime.seconds)
        data.update()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        message={
            "traceback":einfo.traceback,
            "exception":exc.args[0]
        }
        task = tasks.find_one({"_id": task_id})
        data = Task(task_id=task_id, name=task["name"], status="FAILED", start_time=task["start_time"],
                    hostname=task["hostname"], message=message)
        data.update()


        mirror=mirrors.find_one({"_id":task["name"]})
        data=Mirror(task_id=task_id,name=mirror["name"],hostname=mirror["hostname"],status="FAILED",start_time=mirror["start_time"],
                    message=message)
        data.update()

