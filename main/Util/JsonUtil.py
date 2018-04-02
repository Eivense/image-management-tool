import json
from ..Model.Image import Image
def save_json_tofile(data):
    with open('Images.json','w',encoding='utf-8') as json_file:
        json.dump(data,json_file,ensure_ascii=False)


def read_json_toObject(name):
    with open("Images.json",'r',encoding='utf-8') as json_file:
        images=json.load(json_file)
        if name in images:
            return images[name]
        else:
            return Image(name)

def save_object(image):
    with open("Images.json","r",encoding='utf-8') as json_file:
        images=json.load(json_file)
        if image.name in images:
            images[image.name]=image.tojson()
    save_json_tofile(images)