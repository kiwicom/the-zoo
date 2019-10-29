from django.contrib.auth.models import AbstractUser
from django.db import models

from zoo.services.models import Service


class CustomUser(AbstractUser):
    # todo - rename to pinned
    starred_services = models.ManyToManyField(Service)
