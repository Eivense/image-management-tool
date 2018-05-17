from pj.main import app
from pj.main.Celery.Workers import Workers


if __name__ == '__main__':
    workers=Workers.getWorkers()
    workers.start()
    app.run(host='0.0.0.0')
    