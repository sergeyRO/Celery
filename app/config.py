import os

CELERY_BROKER = os.getenv("CELERY_BROKER")
MONGO_DSN = os.getenv("MONGO_DSN")
CELERY_BACKEND = os.getenv("CELERY_BACKEND")
# MONGO_DSN="mongodb://admin:password@127.0.0.1:27017"
# CELERY_BROKER="redis://localhost:6379/1"
# CELERY_BACKEND="redis://localhost:6379/2"