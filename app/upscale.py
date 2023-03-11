import cv2
from cv2 import dnn_superres
from celery_app import celery
import config
import os
from functools import lru_cache
import base64


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
    return output_path