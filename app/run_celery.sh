celery -A celery_app worker -c 1 -l INFO --concurrency=10 -n worker1@localhost
