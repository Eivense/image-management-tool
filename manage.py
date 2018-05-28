import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from pj.main import app
from pj.main.Celery.Workers import Workers

if __name__ == '__main__':
    workers=Workers.getWorkers()
    workers.start()
    app.run(host='0.0.0.0')
    