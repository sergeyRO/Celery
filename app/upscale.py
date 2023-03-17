import numpy as np
from PIL import Image
import cv2
from cv2 import dnn_superres
from celery_app import celery
import os
from functools import lru_cache
from mongoDB import fs, ImageCollection

def mongo_save_file(file):
    imageString = file.tobytes()
    imageID = fs.put(imageString, encoding='utf-8')
    meta = {
        'name': str(imageID),
        'images': [
            {
                'imageID': imageID,
                'shape': file.shape,
                'dtype': str(file.dtype)
            }
        ]
    }
    ImageCollection.insert_one(meta)
    return str(imageID)

def load_file(oid):
    image = ImageCollection.find_one({'name': oid})['images'][0]
    gOut = fs.get(image['imageID'])
    img = np.frombuffer(gOut.read(), dtype=np.uint8)
    img = np.reshape(img, image['shape'])
    res = Image.fromarray(img)
    return res

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
    res = mongo_save_file(result)
    os.remove(input_path)
    #return os.path.basename(output_path)
    return res