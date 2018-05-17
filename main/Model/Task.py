import time
import datetime
from .. import tasks

class Task:
    def __init__(self,name,task_id,hostname,status,start_time=None,end_time=None,message=None,runtime=None):
        self.name=name
        self.task_id=task_id
        self.status=status
        self.start_time=start_time or ""
        self.end_time=end_time or ""
        self.hosthome=hostname
        self.message=message or ""
        self.runtime=runtime or ""

    def convert_to_dict(self):
        data={
            "_id":self.task_id,
            "name":self.name,
            "status":self.status,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "hostname":self.hosthome,
            "message":self.message,
            "runtime":self.runtime
        }
        return data


    def save(self):
        tasks.insert_one(self.convert_to_dict())

    def update(self):
        tasks.update_one({"_id":self.task_id},
                           {"$set":{
                                "_id":self.task_id,
                                "name":self.name,
                                "status":self.status,
                                "start_time":self.start_time,
                                "end_time":self.end_time,
                                "hostname":self.hosthome,
                                "message":self.message,
                                "runtime":self.runtime
                           }
                           })
