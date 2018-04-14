
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

json_path='/home/eivense/code/pj/main/Data/mirrors.json'

rsync_path='/home/eivense/sync_script/rsync.sh'


Workers={

}