from flask import Flask, jsonify, request
from upscale import upscale
from flask import send_from_directory
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
        return jsonify({'link_processed_file': task.result, 'state': task.state})
    else:
        return jsonify({'state': task.state})

@app_flask.route('/processed/<path:filename>', methods=['get'])
def get_file(filename):
    return send_from_directory('uploads', filename)

@app_flask.route('/upscale', methods=['post'])
def picture_mod():
    file = request.files['file_upload']
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        task = upscale.delay(os.path.join(UPLOAD_FOLDER, file.filename),
                             f'./uploads/new_{file.filename}')
        return jsonify({'task_id': task.id})
    else:
        return jsonify({'error': 'Not tasks'})

if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=5001)