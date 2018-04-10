from celery import Celery
from ..Celery.Events import MyEvent
from celery.events.state import Task
import celery

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
        print('{0!r} success'.format(task_id))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
        #super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
