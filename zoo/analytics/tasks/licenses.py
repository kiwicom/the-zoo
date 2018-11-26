from celery import shared_task
from raven.contrib.django.raven_compat.models import client
import requests

from ..models import Dependency, DependencyType


@shared_task
def check_python_lib_licenses():
    session = requests.Session()
    for dependency in Dependency.objects.filter(
        type=DependencyType.PY_LIB.value, license=None
    ).only("name"):
        try:
            response = session.get(f"https://pypi.org/pypi/{dependency.name}/json")
            response.raise_for_status()
            try:
                licenses = {
                    classifier.replace("License :: ", "")
                    .replace("OSI Approved", "")
                    .strip(" :")
                    for classifier in response.json()["info"]["classifiers"]
                    if classifier.startswith("License :: ")
                }
                dependency.license = ", ".join(
                    license for license in licenses if license
                )
            except StopIteration:
                dependency.license = "No license"  # choosealicense.com/no-permission
            dependency.save()
        except requests.RequestException as ex:
            if ex.response.status_code == 404:
                continue

            client.captureException()
