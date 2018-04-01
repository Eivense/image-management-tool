import redis


class Redis:
    @staticmethod
    def connect():
        connection=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
        return connection

    @staticmethod
    def get_all(connection):
        keys=connection.keys()
        return keys

    @staticmethod
    def get(connection,key):
        result=connection.get(key)
        return result