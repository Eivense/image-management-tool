from pymongo import MongoClient

class MongoDB:
    @staticmethod
    def connect():
        client=MongoClient('localhost',27017)
        db=client.celery
        return db.task_queue

    @staticmethod
    def insert(collection,data):
        collection.insert(data)


    @staticmethod
    def find_all(collection):
        results=collection.find()
        list=[]
        for result in results:
            list.append(result)
        return list

    @staticmethod
    def update(connection,id,value):
        connection.update({"_id":id},{"$set":{"end_time":value}})
