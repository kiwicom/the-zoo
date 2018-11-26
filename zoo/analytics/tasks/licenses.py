from celery import shared_task
from raven.contrib.django.raven_compat.models import client
import requests

from ..models import Dependency, DependencyType


@shared_task
def check_python_lib_licenses():
    session = requests.Session()
    for dependency in Dependency.objects.filter(
        type=DependencyType.PY_LIB, license=None
    ).values("name"):
        try:
            response = session.get(f"https://pypi.org/pypi/{dependency.name}/json")
            response.raise_for_status()
            try:
                dependency.license = next(
                    classifier.replace("License :: ").replace("OSI Approved :: ")
                    for classifier in response.json()["info"]["classifiers"]
                    if classifier.startswith("License :: ")
                )
            except StopIteration:
                dependency.license = "No license"  # choosealicense.com/no-permission
            dependency.save()
        except requests.RequestError:
            client.captureException()
