import arrow
from celery import shared_task

from ..services.models import Service
from .mapping import AmazonRancherMapper, GoogleCloudPlatformMapper, map_infra_to_nodes
from .models import InfraNode


@shared_task
def link_service_to_datacenters(service_id):
    service = Service.objects.get(id=service_id)
    amazon = AmazonRancherMapper()
    amazon.link_service_to_datacenters(service)
    gcp = GoogleCloudPlatformMapper()
    gcp.link_service_to_datacenters(service)


@shared_task
def schedule_infra_mapping():
    map_infra_to_nodes()

    InfraNode.objects.filter(
        checked_at__lt=arrow.utcnow().shift(hours=-1).datetime
    ).delete()

    for service in Service.objects.filter(repository_id__isnull=False).all():
        link_service_to_datacenters.delay(service.id)
