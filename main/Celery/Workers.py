import threading
from celery.apps.worker import Worker
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

        node1 = Node(name="worker1@eivense",append="-A pj.main.celery -Q small",extra_args="-B")
        node2 = Node(name="worker2@eivense", append="-A pj.main.celery -Q middle")
        node3 = Node(name="worker3@eivense", append="-A pj.main.celery -Q large -c 1")
        node4 = Node(name="worker4@eivense", append="-A pj.main.celery -Q large")
        node5 = Node(name="worker5@eivense", append="-A pj.main.celery -Q small")
        self.nodelist.extend([node1,node2,node3,node4,node5])

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