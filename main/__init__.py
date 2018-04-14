from flask import Flask
from .Connection.redis_conn import Redis
from .Celery import make_celery

app=Flask(__name__)
app.config.from_pyfile('config.py')
celery=make_celery(app)

redis=Redis.connect()
from .view import *