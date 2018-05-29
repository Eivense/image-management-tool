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

mirror_path= '/usr/local/code/pj/main/Data/mirrors.json'

schedule_path= '/usr/local/code/pj//main/Data/schedule.json'

rsync_path='/home/eivense/sync_script/rsync.sh'

shell_path='/home/eivense/sync_script/'

file_path='/home/eivense/mirror/'

CELERYD_LOG_FILE="/home/eivense/log/%n%I.log"


CELERYD_LOG_LEVEL="info"

CELERYBEAT_SCHEDULE=initSchedule(schedule_path,mirror_path)

normal=Exchange(name="normal",type="direct",durable="true",auto_delete="false")
temp=Exchange(name="temp",type="fanout",durable="true",auto_delete="true")
CELERY_QUEUES={
    Queue(name="small",exchange=normal,routing_key="small",auto_delete="false",durable="false",max_priority="8"),
    Queue(name="middle",exchange=normal,routing_key="middle",auto_delete="false",durable="false",max_priority="9" ),
    Queue(name="large",exchange=normal,routing_key="large",auto_delete="false",durable="false",max_priority="9"),
    Queue(name="temp",exchange=temp,routing_key="temp",auto_delete="true",durable="false",max_priority="10")
}
HOSTNAME="eivense"


CELERY_WORKERS=[
    {"name":"worker1@"+HOSTNAME,"queue":["small"], "concurrency":"2"},
    {"name":"worker2@"+HOSTNAME,"queue":["small","middle"],"concurrency":"2"},
    {"name":"worker3@"+HOSTNAME,"queue":["small","large"],"concurrency":"2"},
    {"name":"temp@"+HOSTNAME,"queue":"temp","concurrency":"1"}
]

