import base64

import cv2
from cv2 import dnn_superres
from celery_app import celery
import os
from functools import lru_cache
from mongoDB import db, fs

# file="C:/Users/serge/Desktop/lama_300px.png"
# with open(file, 'rb') as f:
#     contents = f.read()
# res = fs.put(contents, filename="lama_300px.png")
# print(res)
#
# cursor = db.fs.chunks.find({'files_id': res})
# print(cursor)

def mongo_save_file(file, filename):
    with open(file, 'rb') as f:
        contents = f.read()
    res = fs.put(contents, filename=filename)
    return res
    # cursor = db.fs.chunks.find({'files_id': res})
    # print(cursor)

@lru_cache
def model_cache():
    model_path = "EDSR_x2.pb"
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel('edsr', 2)
    return scaler


@celery.task
def upscale(input_path: str, output_path: str) -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """
    scaler = model_cache()
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    #cv2.imwrite(output_path, result)
    res = mongo_save_file(result, os.path.basename(output_path))
    os.remove(input_path)
    #return os.path.basename(output_path)
    return res
