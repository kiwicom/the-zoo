from collections import defaultdict

from django.db import transaction

from . import amazon, models, rancher
from .models import InfraNode, NodeKind


def url_matches_dns(url, dns_record):
    return all(part in url for part in dns_record.split("*") if part)


@transaction.atomic
def connect_aws_rancher_nodes():
    """Connect AWS EC2 instances' DNS records to Rancher's host DNS records.

    Doesn't create any new nodes.
    """
    aws_ec2_nodes = InfraNode.objects.filter(kind=NodeKind.AWS_EC2_DNS_PRIVATE).all()
    rancher_host_nodes = InfraNode.objects.filter(kind=NodeKind.RANCHER_HOST_DNS).all()

    aws_ec2_dict = {node.value: node for node in aws_ec2_nodes}
    for node in rancher_host_nodes:
        aws_node = aws_ec2_dict.get(node.value)
        if aws_node is not None:
            node.sources.add(aws_node)


def map_infra_to_nodes():
    """Map infrastructure from all datacenters to the InfraNode table."""
    amazon.map_to_nodes()
    rancher.map_to_nodes()
    connect_aws_rancher_nodes()


class Mapper:
    """Abstract class to help retrieve data from ``InfraNode``s."""

    def __init__(self):
        self._components_cache = {}
        self._members_cache = {}

    def get_service_image_nodes(self, service):
        image_uuid_part = f"{service.repository.owner}/{service.repository.name}"
        return InfraNode.objects.filter(
            kind=NodeKind.DOCKER_IMAGE_UUID, value__contains=image_uuid_part
        )

    def link_service_to_datacenters(self, service):
        for image_node in self.get_service_image_nodes(service):
            self.link_image_to_service(image_node, service)

    @transaction.atomic
    def link_image_to_service(self, image_node, service):
        raise NotImplementedError()


class AmazonRancherMapper(Mapper):
    """Retrieve data from Amazon and Rancher infrastructure and store it."""

    def _get_component_urls(self, component):
        portrules = component.find_sources_by_kind(NodeKind.RANCHER_LB_PORTRULE_URI)
        if not portrules:
            return [
                node.value
                for node in component.find_sources_by_kind(NodeKind.AWS_RECORD_SET_DNS)
            ]

        urls = []
        for portrule_node in portrules:
            for node in portrule_node.find_sources_by_kind(NodeKind.AWS_RECORD_SET_DNS):
                if url_matches_dns(portrule_node.value, node.value):
                    urls.append(portrule_node.value)
        return urls

    def _get_component_data(self, component, project):
        if component.value in self._components_cache:
            return self._components_cache[component.value]

        name = rancher.get_service(project.value, component.value).get("name")
        urls = self._get_component_urls(component)
        result = {"name": name, "urls": urls}

        self._components_cache[component.value] = result
        return result

    def _get_project_members(self, project):
        if project.value not in self._members_cache:
            self._members_cache[project.value] = rancher.parse_members_from_project(
                rancher.get_project(project.value)
            )
        return self._members_cache[project.value]

    def _get_amazon_datacenters(self, component_node, service):
        datacenters = []
        for elb_node in component_node.find_sources_by_kind(NodeKind.AWS_ELB_DNS):
            _, zone, _ = elb_node.value.split(".", 2)

            datacenter, _ = models.Datacenter.objects.get_or_create(
                provider="Amazon", region=zone
            )
            service_datacenter, _ = models.ServiceDatacenter.objects.get_or_create(
                service=service, datacenter=datacenter
            )
            datacenters.append(service_datacenter)
        return datacenters

    @transaction.atomic
    def link_image_to_service(self, image_node, service):
        datacenters_components = defaultdict(set)

        for component in image_node.find_sources_by_kind(NodeKind.RANCHER_SERVICE_ID):
            datacenters = self._get_amazon_datacenters(component, service)

            for project in component.find_sources_by_kind(NodeKind.RANCHER_PROJ_ID):
                component_data = self._get_component_data(component, project)
                project_members = self._get_project_members(project)

                for service_datacenter in datacenters:
                    models.ServiceDatacenterComponent.objects.get_or_create(
                        service_datacenter=service_datacenter, **component_data
                    )
                    # save service_datacenter id with its components for later deletion
                    datacenters_components[service_datacenter.id].add(
                        component_data["name"]
                    )
                    for name in project_members:
                        models.ServiceDatacenterMember.objects.get_or_create(
                            service_datacenter=service_datacenter, name=name
                        )
                    models.ServiceDatacenterMember.objects.filter(
                        service_datacenter=service_datacenter
                    ).exclude(name__in=project_members).delete()

        # delete no longer existing services in datacenters
        for datacenter_id in datacenters_components:
            models.ServiceDatacenterComponent.objects.filter(
                service_datacenter_id=datacenter_id
            ).exclude(name__in=datacenters_components[datacenter_id]).delete()
