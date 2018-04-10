class Task:
    def __init__(self,task_name,task_id,hostname,status=None,starttime=None):
        self.task_name=task_name
        self.task_id=task_id
        self.status=""
        self.starttime=""
        self.endtime=""
        self.hosthome=hostname
        self.exitcode_message=""

    def convert_to_dict(self):
        result={
            "task_name":self.task_name,
            "task_id":self.task_id,
            "status":self.status,
            "start_time":self.starttime,
            "end_time":self.endtime,
            "hostname":self.hosthome,
            "message":self.exitcode_message
        }
        return result