from django.views.generic import ListView

from . import models


class RepoList(ListView):
    model = models.Repository
