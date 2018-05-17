import os
import time
from flask import jsonify, request, send_from_directory
from flask_uploads import UploadSet, SCRIPTS, configure_uploads, UploadNotAllowed

from . import app, control, inspect
from . import mirrors, tasks
from .Celery.Workers import Workers
from .Celery.celery_tasks import test
from .config import UPLOADED_SHELL_DEST
from .Model.Task import Task
from .Model.Mirror import Mirror
scripts=UploadSet("shell",SCRIPTS)
configure_uploads(app,scripts)

@app.route('/')
def hello_world():
    return "hello world"


@app.route('/rsync')
def flask_rsync():
    list=['elvish','inna','putty','vim']
    result=[]
    for i in list:
        task=test.apply_async(args=[i,"mirrors.shu.edu.cn"],queue='small')
        result.append(task.id)
    return jsonify(result)

@app.route('/single/<name>/<upstream>')
def single(name,upstream):
    active=inspect.active()#正在执行的
    reserved=inspect.reserved()#等待执行的

    for workername in active:
        worker=active[workername]
        if (worker):
            for task in worker:
                args=eval(task["args"])
                mirror=args[0]
                if(name==mirror):
                    terminate_task(task_id=task["id"],type="active")

    for workername in reserved:
        worker=reserved[workername]
        if (worker):
            for task in worker:
                args = eval(task["args"])
                mirror=args[0]
                if(name==mirror):
                    control.terminate(task_id=task["id"],type="reserved")

    task=test.apply_async(args=[name,upstream],queue='temp')
    return jsonify(task.id)

@app.route('/task_status')
def get_task():
    result=mirrors.find()
    data={}
    for mirror in result:
        data[mirror["_id"]]=mirror
    return jsonify(data)

@app.route('/worker_info')
def worker_info():
    return jsonify(inspect.stats())

@app.route('/active')
def active():
    return jsonify(inspect.active())

@app.route('/reserved')
def reserved():
    return jsonify(inspect.reserved())

@app.route('/terminate/<task_id>/<type>')
def terminate_task(task_id,type):
    control.terminate(task_id=task_id)
    if(type=="active"):
        task=tasks.find_one({"_id":task_id})
        if(task):
            data = Task(task_id=task_id, name=task["name"], status="REVOKED",start_time=task["start_time"],
                        hostname=task["hostname"],message="Revoked", runtime="")
            data.update()
            mirror=mirrors.find_one({'task_id':task_id})
            if(mirror):
                data=Mirror(task_id=mirror["task_id"],name=mirror["_id"],status="REVOKED",start_time=mirror["start_time"],
                            hostname=mirror["hostname"],message="Revoked")
                data.update()
                return jsonify(task_id)
    elif(type=="reserved"):
        pass
        # list=inspect.reserved()
        # for workername in list:
        #     worker = list[workername]
        #     if (worker):
        #         for task in worker:
        #             if (task["id"] == task_id):
        #                 data = Task(task_id=task_id, name=eval(task["args"])[0], status="REVOKED",
        #                             hostname=task["hostname"], message="Revoked", runtime="")
        #                 data.save()
    return jsonify(task_id)





@app.route('/kill')
def kill_all():
    workers=Workers.getWorkers()
    workers.kill()
    return "success"


@app.route('/stop')
def stop_all():
    workers=Workers.getWorkers()
    workers.stopAll()
    return "success"


@app.route('/upload_shell',methods=['POST','GET','OPTIONS'])
def file_upload():
    if request.method=="POST" and 'file' in request.files:
        try:
            scripts.save(request.files['file'])
            file_dir=UPLOADED_SHELL_DEST
        except UploadNotAllowed:
            return jsonify("uploadNotAllowed")
        else:
            for root,dirs,files in os.walk(file_dir):
                return jsonify(list(files))
    else:
        return jsonify("failed")


@app.route('/script_list')
def script_list():
    file_dir=UPLOADED_SHELL_DEST
    for root,dirs,files in os.walk(file_dir):
        return jsonify(files)

@app.route('/download/<filename>')
def download(filename):
    if request.method=="GET":
        if os.path.isfile(os.path.join(UPLOADED_SHELL_DEST,filename)):
            return send_from_directory(UPLOADED_SHELL_DEST,filename,as_attachment=True)




@app.route('/search/<data>/<pageSize>/<currentPage>')
def search(data,pageSize,currentPage):
    result=tasks.find({'name':data}).skip((int(currentPage)-1)*int(pageSize)).limit(int(pageSize))
    totalsize=result.count()
    list=[]
    for task in result:
        list.append(task)
    data={
        "totalsize":totalsize,
        "result":list
    }
    return jsonify(data)