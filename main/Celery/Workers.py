import threading
from celery.apps.multi import Cluster,Node
from ..config import CELERY_WORKERS,CELERYD_LOG_FILE
import signal

class Workers:
    cluster=None
    beat=None
    nodelist=[]

    __instance_lock = threading.Lock()
    @classmethod
    def getWorkers(cls):
        if not hasattr(Workers,"_instance"):
            with Workers.__instance_lock:
                if not hasattr(Workers,"_instance"):
                    Workers._instance=Workers()
        return Workers._instance

    def __init__(self):
        extra="-B"

        for worker in CELERY_WORKERS:
            queue=""
            if(len(worker.get("queue"))>1):
                queue=",".join(worker.get("queue"))
            else:
                queue=worker.get("queue")[0]
            node = Node(name=worker.get("name"),
                        append="-A celery"
                               + " -Q " + queue
                               + " --concurrency " + worker.get("concurrency")
                               + " -l info"
                               + " -f " + CELERYD_LOG_FILE,
                        extra_args=extra
                        )
            self.nodelist.append(node)
            extra=""
        cluster = Cluster(self.nodelist)
        self.cluster=cluster


    def createNewWorker(self,name,queue):
        node=Node(name=name,
                  append="-A pj.main.celery"
                         + " -Q " + queue
                         + " -l info"
                         + " -f " + CELERYD_LOG_FILE)
        self.nodelist.append(node)
        node.start()

    def start(self):
        self.cluster.start()

    def removeNode(self,name):
        for node in self.nodelist:
            if node.name==name:
                node.send(signal.SIGTERM)
                self.nodelist.remove(node)



    def kill(self):
        self.cluster.kill()

    def stopAll(self):
        self.cluster.stop()

    def restart(self):
        self.cluster.restart(sig=15)

    def findworker(self,name):
        worker=self.cluster.find(name)
        return worker.alive()