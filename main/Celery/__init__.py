from celery import Celery
from ..Celery.Events import MyEvent
import celery
from ..Util.Util import *
from ..config import json_path
def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery



class BaseTask(celery.Task):
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        success = {
            "task_id": task_id
        }
        save_object(success, "success", '/home/eivense/code/pj/test.json')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        mirrors=read_json(json_path)
        task_name = args
        task_name = task_name[2:]
        task_name = task_name[:-2]
        mirrors[task_name]["status"]="FAILED"
        mirrors[task_name]["message"]=einfo
        save_object(mirrors, "fail", '/home/eivense/code/pj/test.json')
        #super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
