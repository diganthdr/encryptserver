from os import times
from flask import Flask
from worker.tasks import make_celery
from driver import request_router

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)


@celery.task()
def router_task(filepath, operation):
    driver_response = request_router(filepath, operation)
    return driver_response
