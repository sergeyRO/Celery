import cv2
from cv2 import dnn_superres
from celery import Celery
import os

from config import CELERY_BROKER, MONGO_DSN, CELERY_BACKEND
#backend=f"{MONGO_DSN}"
celeryApp = Celery('app', backend=CELERY_BACKEND, broker=CELERY_BROKER)


@celeryApp.task
def upscale(input_path: str, output_path: str, model_path: str = "app\EDSR_x2.pb") -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """
    print(input_path)
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel('edsr', 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)
    #os.remove(input_path)



#def example():
#    upscale('lama_300px.png', 'lama_600px.png')
