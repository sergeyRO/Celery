#import nanoid
#import waitress
from flask import Flask, jsonify, request
from view import UpscaleView, TaskView, FileView
from flask_pymongo import PyMongo
#from upscale import celeryApp

import config

app = Flask(__name__)
mongo = PyMongo(app, uri=config.MONGO_DSN)
#backend=f"{MONGO_DSN}"


app.add_url_rule('/tasks/<task_id>', view_func=TaskView.as_view('task_status'), methods={'GET'})
app.add_url_rule('/processed/<string:file>', view_func=FileView.as_view('processed_file'), methods={'GET'})
app.add_url_rule('/upscale', view_func=UpscaleView.as_view('get_file'), methods={'POST'})
app.run()
#debug=True, host='0.0.0.0', port=5000


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