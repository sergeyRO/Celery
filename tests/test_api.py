import pytest
import time
import requests


def test_Upscale(request):
    file = {"file_upload": open("./tests/cherep.png", "rb")}
    response = requests.post('http://127.0.0.1:5001/upscale', files=file)
    assert response.status_code == 200
    task_id = response.json()['task_id']
    request.config.cache.set('task_id', task_id)

def test_status_load(request):
    while True:
        response = requests.get(f'http://127.0.0.1:5001/tasks/{request.config.cache.get("task_id", None)}')
        if response.json()['state'] == 'PENDING':
            assert response.status_code == 200
        elif response.json()['state'] == 'SUCCESS':
            assert response.json()['state'] == 'SUCCESS'
            file_id = response.json()['file_id']
            request.config.cache.set('file_id', file_id)
            break
        time.sleep(30)

def test_file(request):
    response = requests.get(f'http://127.0.0.1:5001/processed/{request.config.cache.get("file_id", None)}')
    assert response.status_code == 200