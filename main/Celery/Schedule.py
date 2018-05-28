from ..Util.Util import *
from celery.schedules import crontab
def initSchedule(schedule_path,mirrors_path):
    CELERYBEAT_SCHEDULE={}
    MIRRORS={}
    schedules=read_json(schedule_path)
    mirror_schedule=schedules["rsync"]
    for mirror in mirror_schedule:
        data=mirror_schedule[mirror]
        schedule_time=data["schedule_time"]
        upstream=data["upstream"]
        time=schedule_time.split("-")
        CELERYBEAT_SCHEDULE[mirror] ={
            'task':'rsync',
            'schedule':crontab(day_of_week=time[0],hour=time[1],minute=time[2]),
            'args':[mirror,upstream],
            'options':{"queue":data["queue"],"routing_key":data["queue"]}
        }
        MIRRORS[mirror]={
            "task_id":"",
            "start_time":"",
            "hostname":"",
            "status":"",
            "last_succeed":"",
            "end_time":"",
            "message":""
        }
    save_json_tofile(MIRRORS,mirrors_path)
    return CELERYBEAT_SCHEDULE
