class Image:
    def __init__(self,name,status):
        self.name=name
        self.status="pending"

    def tojson(self):
        result = {
            "name": self.name,
            "status": self.status,
        }
        return result

    @staticmethod
    def toObject(json):
        name=json["name"]
        status=json["status"]
        return Image(name,status)