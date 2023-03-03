#import nanoid
from flask import Flask, jsonify, request
from views import UpscaleView, TaskView, FileView
from flask_pymongo import PyMongo
from errors import ApiException

import config
from celery_app import celery_app

app = Flask("app")

mongo = PyMongo(app, uri=config.MONGO_DSN)

celery_app.conf.update(app.config)

@app.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify(
        {
            'status': 'error',
            'message': error.message
        }
    )
    response.status_code = error.status_code
    return response



app.add_url_rule('/tasks/<string:task_id>', view_func=TaskView.as_view('task_status'), methods={'GET'})
app.add_url_rule('/processed/<string:file>', view_func=FileView.as_view('processed_file'), methods={'GET'})
app.add_url_rule('/upscale', view_func=UpscaleView.as_view('get_file'), methods={'POST'})
app.run()



'''
class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask


class Comparison(MethodView):
    def get(self, task_id):
        task = get_task(task_id)
        return jsonify({"status": task.status, "result": task.result})

    def post(self):
        image_ids = [self.save_image(field) for field in ("image_1", "image_2")]
        task = match_photos.delay(*image_ids)
        return jsonify({"task_id": task.id})

    def save_image(self, field) -> str:
        image = request.files.get(field)
        return str(mongo.save_file(f"{nanoid.generate()}{image.filename}", image))


comparison_view = Comparison.as_view("comparison")
app.add_url_rule(
    "/comparison/<string:task_id>", view_func=comparison_view, methods=["GET"]
)
app.add_url_rule("/comparison/", view_func=comparison_view, methods=["POST"])
'''