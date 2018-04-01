from flask import Flask
from .Celery import make_celery



app=Flask(__name__)
app.
celery=make_celery(app)
# celery = Celery(app.name,
#                 broker='amqp://localhost',
#                 backend='redis://localhost')


from .view import *