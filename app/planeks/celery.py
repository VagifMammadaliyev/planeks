import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planeks.settings")

app = Celery("planeks")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


class QUEUES:
    GENERATOR_QUEUE = "generator"
