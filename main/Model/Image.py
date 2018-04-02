class Image:
    def __init__(self,name):
        self.name=name
        self.status="pending"

    def tojson(self):
        result = {
            "task_name": self.name,
            "status": self.status,
        }
        return result

