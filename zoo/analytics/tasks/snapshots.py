from celery import shared_task

from .. import models


@shared_task
def take_dependency_snapshots():
    for dependency in models.Dependency.objects.all():
        snapshot = models.DependencySnapshot(
            dependency=dependency, dep_usages_num=dependency.depusage.count()
        )
        snapshot.full_clean()
        snapshot.save()
