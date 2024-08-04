from flask import current_app as app
from celery import Celery
import redis

celery = Celery("backend jobs")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)