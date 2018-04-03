import json
from ..Model.Image import Image
def save_json_tofile(data):
    with open('/home/eivense/code/pj/Images.json','w',encoding='utf-8') as json_file:
        json.dump(data,json_file,ensure_ascii=False)


def read_json_toObject(name):
    with open("/home/eivense/code/pj/Images.json",'r',encoding='utf-8') as json_file:
        images=json.load(json_file)
        print(name)
        if name in images:
            return Image.toObject(images[name])
        else:
            return Image(name,"pending")

def save_object(image):
    with open("/home/eivense/code/pj/Images.json","r",encoding='utf-8') as json_file:
        images=json.load(json_file)
        name=image.name
        print(name)
        if name in images:
            images[name]=image.tojson()
    save_json_tofile(images)