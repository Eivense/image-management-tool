import threading

from celery.apps.multi import Cluster,Node

class Workers:
    __instance_lock=threading.Lock()
    cluster=None
    nodelist=[]

    @classmethod
    def getWorkers(cls):
        if not hasattr(Workers,"_instance"):
            with Workers.__instance_lock:
                if not hasattr(Workers,"_instance"):
                    Workers._instance=Workers(5)
        return Workers._instance

    def __init__(self,nums):
        for i in range(1, nums + 1):
            node = Node(name="worker" + str(i) + "@eivense")
            self.nodelist.append(node)
        cluster = Cluster(self.nodelist)
        self.cluster=cluster


    def createNewWorker(self,name):
        node=Node(name=name)
        self.nodelist.append(node)
        node.start()

    def start(self):
        self.cluster.start()

    def kill(self):
        self.cluster.kill()

    def stopAll(self):
        self.cluster.stop()


    def findworker(self,name):
        worker=self.cluster.find(name)
        return worker.alive()