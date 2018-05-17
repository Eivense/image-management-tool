import json
import fcntl



def save_json_tofile(data,path):
    with open(path,'w',encoding='utf-8') as json_file:
        fcntl.flock(json_file,fcntl.LOCK_EX)
        json.dump(data,json_file,ensure_ascii=False)
        fcntl.flock(json_file,fcntl.LOCK_UN)

def save_object(task,name,path):
    with open(path,"r",encoding='utf-8') as json_file:
        fcntl.flock(json_file,fcntl.LOCK_EX)
        images=json.load(json_file)
        images[name]=task
        fcntl.flock(json_file, fcntl.LOCK_UN)
        save_json_tofile(images,path)


def read_json(path):
    with open(path,'r',encoding='utf-8') as json_file:
        fcntl.flock(json_file,fcntl.LOCK_EX)
        result=json.load(json_file)
        fcntl.flock(json_file, fcntl.LOCK_UN)
        return result


def rsync_exitcode(code):
    return {
        0:"Success",
        1:"Syntax or usage error",
        2:"Protocol incompatibility",
        3:"Errors selecting input / output files, dirs",
        4:"Requested action not supported: an attempt was made to manipulate "
          "64 - bit files on a platform that cannot support them; or an option was"
          "specified that is supported by the client and not by the server.",
        5:"Error starting client - server protocol",
        6:"Daemon unable to append to log - file",
        10:"Error in socket I / O",
        11:"Error in file I / O",
        12:"Error in rsync protocol Data stream",
        13:"Errors with program diagnostics",
        14:"Error in IPC code",
        20:"Received SIGUSR1 or SIGINT",
        21:"Some error returned by waitpid()",
        22:"Error allocating core memory buffers",
        23:"Partial transfer due to error",
        24:"Partial transfer due to vanished source files",
        25:"The --max-delete limit stopped deletions",
        30:"Timeout in Data send / receive",
        35:"Timeout waiting for daemon connection",
        126:"No execution permissions"
    }.get(code)