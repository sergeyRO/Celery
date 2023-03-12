celery -A celery_app worker -c 4 -l INFO --concurrency=10 -n worker1@localhost
