from flask import Flask
from .Celery import make_celery



app=Flask(__name__)
app.config.from_pyfile('config.py')
celery=make_celery(app)


from .view import *