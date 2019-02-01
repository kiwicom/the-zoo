from ddtrace import patch_all

from .base.celery import app as celery_app
from .base.wsgi import application

patch_all(requests=True)
