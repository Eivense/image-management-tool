from .. import mirrors
class Mirror:
    def __init__(self,name,task_id,hostname,status,start_time,end_time=None,message=None,lastsucceed=None):
        self.name=name
        self.task_id=task_id
        self.status=status
        self.start_time=start_time
        self.end_time=end_time or ""
        self.hosthome=hostname
        self.message=message or ""
        self.lastsucceed=lastsucceed or ""

    def convert_to_dict(self):
        data={
            "_id":self.name,
            "task_id":self.task_id,
            "status":self.status,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "hostname":self.hosthome,
            "last_succeed":self.lastsucceed,
            "message":self.message
        }
        return data

    def save(self):
        if(mirrors.find_one({"_id":self.name})):
            self.update()
        else:
            mirrors.insert_one(self.convert_to_dict())

    def update(self):
        mirrors.update_one({"_id":self.name},
                           {"$set":{
                                "task_id":self.task_id,
                                "status":self.status,
                                "start_time":self.start_time,
                                "end_time":self.end_time,
                                "hostname":self.hosthome,
                                "last_succeed":self.lastsucceed,
                                "message":self.message
                           }
                           })