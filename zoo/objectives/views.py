from django.views.generic import ListView

from . import models


class ObjectiveList(ListView):
    model = models.Objective
