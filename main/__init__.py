from flask import Flask
from pymongo import MongoClient
from .Celery import make_celery
from .config import MONGODB
from flask_cors import *
from celery.app.control import Control,Inspect
app=Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_pyfile('config.py')
celery=make_celery(app)
control=Control(app=celery)
inspect=Inspect(app=celery)
mongo=MongoClient(MONGODB)
db=mongo.celery
tasks=db.tasks
mirrors=db.mirrors
from .view import *