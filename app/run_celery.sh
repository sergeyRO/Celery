celery -A celery_app worker -l INFO --concurrency=10 -n worker1@localhost
celery -A celery_app worker -l INFO --concurrency=10 -n worker2@localhost
celery -A celery_app worker -l INFO --concurrency=10 -n worker3@localhost
