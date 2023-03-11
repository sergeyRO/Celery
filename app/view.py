from flask.views import MethodView
from flask import jsonify, request
from upscale import upscale
from flask import send_from_directory
import os

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UpscaleView(MethodView):
    def post(self):
        file = request.files['file_upload']
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            task = upscale.delay(os.path.join(UPLOAD_FOLDER, file.filename),
                                 f'./uploads/new{file.filename}')
            return jsonify({'task_id': task.id})
        else:
            return jsonify({'error': 'Not tasks'})


class TaskView(MethodView):
    def get(self, task_id: str):
        print(task_id)
        task = upscale.AsyncResult(task_id)
        #result = task.get(timeout=5)
        if task.state == 'SUCCESS':
            return jsonify({'link_processed_file': task.result, 'state': task.state})
        else:
            return jsonify({'state': task.state})


class FileView(MethodView):
    def get(self, filename):
        return send_from_directory('uploads', filename)
