import os

CELERY_BROKER = os.getenv("CELERY_BROKER")
MONGO_DSN = os.getenv("MONGO_DSN")
CELERY_BACKEND = os.getenv("CELERY_BACKEND")
# MONGO_DSN="mongodb://app:1234_secret@127.0.0.1:27017/files?authSource=admin"
# CELERY_BROKER="redis://127.0.0.1:6379/1"
# CELERY_BACKEND="redis://127.0.0.1:6379/2"

#PG_DSN = os.getenv("PG_DSN")
