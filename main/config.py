from kombu import Exchange, Queue
from pj.main.Celery.Schedule import initSchedule

BROKER_URL='amqp://localhost'

MONGODB='mongodb://localhost:27018/'

CELERY_RESULT_BACKEND='redis://localhost'

CELERY_TASK_RESULT_EXPIRES=60*60*24

CELERY_TRACK_STARTED=True

CELERYD_FORCE_EXECV=True

CELERY_SEND_EVENTS=True

#并发数量
CELERYD_CONCURRENCY = 2
#每个worker最大任务执行数
CELERYD_MAX_TASKS_PER_CHILD = 100
#任务预取数  从消息队列中取得的任务数  小任务 应该设置的大一点
CELERYD_PREFETCH_MULTIPLIER = 100

UPLOADED_SHELL_DEST='/home/eivense/sync_script'

mirror_path= '/home/eivense/code/pj/main/Data/mirrors.json'

schedule_path= '/home/eivense/code/pj/main/Data/schedule.json'

rsync_path='/home/eivense/sync_script/rsync.sh'

shell_path='/home/eivense/sync_script/'

file_path='/home/eivense/mirror/'

CELERYD_LOG_FILE="/home/eivense/log/%n%I.log"


CELERYD_LOG_LEVEL="info"

CELERYBEAT_SCHEDULE=initSchedule(schedule_path,mirror_path)

normal=Exchange(name="normal",type="direct",durable="false",auto_delete="true")
temp=Exchange(name="temp",type="direct",durable="false",auto_delete="true")
CELERY_QUEUES={
    Queue("small",exchange=normal,routing_key="small",auto_delete="true",durable="false"),
    Queue("middle",exchange=normal,routing_key="middle",auto_delete="true",durable="false"),
    Queue("large",exchange=normal,routing_key="large",auto_delete="true",durable="false"),
    Queue("temp",exchange=temp,routing_key="temp",auto_delete="true",durable="false")
}
hostname="eivense"
CELERY_WORKERS=[
    {
        "name":"worker1@"+hostname,
        "queue":"small",
        "concurrency":"2"
     },
    {
        "name":"worker2@"+hostname,
        "queue":"small",
        "concurrency":"2"
     },
    {
        "name":"worker3@"+hostname,
        "queue":"middle",
        "concurrency":"2"
    },
    {
        "name":"temp@"+hostname,
        "queue":"temp",
        "concurrency":"1"
    }
]

