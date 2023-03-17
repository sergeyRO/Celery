import csv
import io

from flask import Flask, jsonify, request
from upscale import upscale, load_file
from flask import send_file
import os


app_flask = Flask(__name__)


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app_flask.route('/tasks/<task_id>', methods=['get'])
def tasks(task_id: str):
    print(task_id)
    task = upscale.AsyncResult(task_id)
    # result = task.get(timeout=5)
    if task.state == 'SUCCESS':
        return jsonify({'file_id': task.result, 'state': task.state})
    else:
        return jsonify({'state': task.state})

@app_flask.route('/processed/<oid>', methods=['get'])
def get_file(oid):
    pil_img = load_file(oid)
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app_flask.route('/upscale', methods=['post'])
def picture_mod():
    file = request.files['file_upload']
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        # task = upscale.delay(os.path.join(UPLOAD_FOLDER, file.filename),
        #                      f'./uploads/new_{file.filename}')
        task = upscale.delay(os.path.join(UPLOAD_FOLDER, file.filename), f'./uploads/new_{file.filename}')
        return jsonify({'task_id': task.id})
    else:
        return jsonify({'error': 'Not tasks'})

if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=5001)