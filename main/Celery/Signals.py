from celery.signals import after_task_publish


@after_task_publish.connect
def task_sent_handler(sender=None,headers=None,body=None,**kwargs):
    info=headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))