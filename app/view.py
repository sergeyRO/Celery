from flask.views import MethodView
from flask import jsonify, request
from upscale import upscale

import os

UPLOAD_FOLDER = 'app'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UpscaleView(MethodView):
    def post(self):
        file = request.files['file_upload']
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            #upscale(os.path.join(UPLOAD_FOLDER, file.filename), os.path.join(UPLOAD_FOLDER, f'new{file.filename}'))
            task = upscale.delay(os.path.join(UPLOAD_FOLDER, file.filename), os.path.join(UPLOAD_FOLDER, f'new{file.filename}'))

        # print(request.json['file'])
        # upscale(request.json["file"], f'new{request.json["file"]}')
            return jsonify({'task_id': task.id})
            #return jsonify({'task_id': task})
        else:
            return jsonify({'error': 'Not tasks'})


class TaskView(MethodView):
    def get(self, task_id: str):
        task = upscale.AsyncResult(task_id)
        result = task.get(timeout = 3)
        return jsonify({'link_processed_file': result, 'state': task.state})


class FileView(MethodView):
    def get(self, file: str):
        ...
        # data_ads = request.json
        # with Session() as session:
        #     new_ads = Ads(**data_ads)
        #     session.add(new_ads)
        #     session.commit()
        return jsonify({'file': 'file'})
