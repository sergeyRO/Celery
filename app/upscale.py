import base64

import cv2
from cv2 import dnn_superres
from celery_app import celery
import os
from functools import lru_cache
from config import MONGO_DSN
import pymongo
from bson.binary import Binary

client = pymongo.MongoClient({MONGO_DSN}, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

# def insert_image(request):
#     with open(request.GET["image_name"], "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     print(encoded_string)
#     abc=db.database_name.insert({"image":encoded_string})
#     return HttpResponse("inserted")

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
    cv2.imwrite(output_path, result)
    os.remove(input_path)
    mongo.save_file(os.path.basename(output_path), result)
    return os.path.basename(output_path)
    #return result