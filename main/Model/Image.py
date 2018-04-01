class Image:
    def __init__(self,name,status):
        self.name=name
        self.status=status
        self.exit_code=""

    def convert_to_dict(self):
        result = {
            "task_name": self.name,
            "status": self.status,
            "exit_code":self.exit_code,
        }
        return result
