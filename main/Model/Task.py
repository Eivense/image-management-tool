class Task:
    def __init__(self,task_id,task_name,starttime,hostname):
        self.task_id=task_id
        self.task_name=task_name
        self.starttime=starttime
        self.endtime=""
        self.hosthome=hostname

    def convert_to_dict(self):
        result={
            "_id":self.task_id,
            "task_name":self.task_name,
            "start_time":self.starttime,
            "end_time":self.endtime,
            "hostname":self.hosthome,
        }
        return result