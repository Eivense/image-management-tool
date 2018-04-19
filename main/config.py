from kombu import Exchange, Queue
from pj.main.Celery.Schedule import initSchedule

BROKER_URL='amqp://localhost'

CELERY_RESULT_BACKEND='redis://localhost'

CELERY_TASK_RESULT_EXPIRES=60*60*24

CELERY_TRACK_STARTED=True

CELERY_TIMEZONE='Asia/Shanghai'

CELERYD_FORCE_EXECV=True

CELERY_SEND_EVENTS=True

#并发数量
CELERYD_CONCURRENCY = 2
#每个worker最大任务执行数
CELERYD_MAX_TASKS_PER_CHILD = 100
#任务预取数  从消息队列中取得的任务数  小任务 应该设置的大一点
CELERYD_PREFETCH_MULTIPLIER = 100

mirror_path= '/home/eivense/code/pj/main/Data/mirrors.json'
schedule_path= '/home/eivense/code/pj/main/Data/schedule.json'

rsync_path='/home/eivense/sync_script/rsync.sh'


# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'rsync',
#         'schedule': crontab(hour=8, minute=50, day_of_week=3),
#         'args':["elvish"],
#         'options':{'routing_key':'small','queue':'small'}
#     },
# }
CELERYBEAT_SCHEDULE=initSchedule(schedule_path,mirror_path)
CELERY_QUEUES={
    Queue('small',routing_key='small'),
    Queue('middle',routing_key='middle'),
    Queue('large',routing_key='large')
}

