from celery import Celery
from config import CELERY_BROKER, MONGO_DSN, CELERY_BACKEND


celery = Celery('proj', backend=CELERY_BACKEND, broker=CELERY_BROKER, include=['upscale'])
#app.conf.update(app.config)