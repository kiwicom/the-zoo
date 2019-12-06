from collections import defaultdict

import requests
from django.db import transaction

from . import amazon, gcp, models, rancher
from .models import Datacenter, InfraNode, NodeKind
from .utils import GCPClient, KubernetesClient


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
    gcp.map_to_nodes()


class Mapper:
    """Abstract class to help retrieve data from ``InfraNode``s."""

    def __init__(self):
        self._components_cache = {}
        self._members_cache = {}

    def _create_component(self, service_datacenter, component_data):
        if not component_data:
            return

        try:
            models.ServiceDatacenterComponent.objects.get(
                service_datacenter_id=service_datacenter.id, name=component_data["name"]
            )
        except models.ServiceDatacenterComponent.DoesNotExist:
            models.ServiceDatacenterComponent.objects.create(
                service_datacenter=service_datacenter, **component_data
            )

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


class GoogleCloudPlatformMapper(Mapper):
    def _get_ingress_component(self, workload):
        # we assume that all our services use unique namespaces
        # and use ingress for routing requests
        if workload.value in self._components_cache:
            return self._components_cache[workload.value]

        # zoo.datacenters.gcp._workload_identifier
        cluster, _, full_name = workload.value.split(":")
        namespace, _ = full_name.split("/")
        hosts = set()

        gcloud = GCPClient()
        kube = KubernetesClient(gcloud.get_clusters_by_name(cluster))

        for ingress in kube.get_ingress(namespace):
            hosts = hosts.union(
                {rule.host for rule in ingress.spec.rules if rule.host is not None}
            )

        result = {"name": namespace, "urls": list(hosts)}

        self._components_cache[workload.value] = result
        return result

    def _get_project_members(self, project):
        gcloud = GCPClient()
        if project.value not in self._members_cache:
            self._members_cache[project.value] = gcloud.get_project_owners(
                project.value
            )
        return self._members_cache[project.value]

    def _get_gcp_datacenter(self, cluster, service):
        _, _, zone, _ = cluster.value.split("_")

        datacenter, _ = models.Datacenter.objects.get_or_create(
            provider=Datacenter.PROVIDER_GCP, region=zone
        )
        service_datacenter, _ = models.ServiceDatacenter.objects.get_or_create(
            service=service, datacenter=datacenter
        )
        return service_datacenter

    @transaction.atomic
    def link_image_to_service(self, image_node, service):
        ingress_components = defaultdict(set)

        for cluster in image_node.find_sources_by_kind(NodeKind.GCP_CLUSTER_NAME):
            datacenter = self._get_gcp_datacenter(cluster, service)

            for project in cluster.find_sources_by_kind(NodeKind.GCP_PROJ_ID):
                project_members = self._get_project_members(project)

                for member in project_members:
                    models.ServiceDatacenterMember.objects.get_or_create(
                        service_datacenter=datacenter,
                        name=member["name"],
                        email=member["email"],
                    )
                models.ServiceDatacenterMember.objects.filter(
                    service_datacenter=datacenter
                ).exclude(
                    name__in={member["name"] for member in project_members}
                ).delete()

        for workload in image_node.find_sources_by_kind(NodeKind.GCP_WORKLOAD_NAME):
            component_data = self._get_ingress_component(workload)
            self._create_component(datacenter, component_data)

            if component_data:
                # save datacenter id with its component for later deletion
                ingress_components[datacenter.id].add(component_data["name"])

        # delete no longer existing ingress in datacenters
        for datacenter_id in ingress_components:
            models.ServiceDatacenterComponent.objects.filter(
                service_datacenter_id=datacenter_id
            ).exclude(name__in=ingress_components[datacenter_id]).delete()


class AmazonRancherMapper(Mapper):
    """Retrieve data from Amazon and Rancher infrastructure and store it."""

    def _get_component_urls(self, component):
        portrules = component.find_sources_by_kind(NodeKind.RANCHER_LB_PORTRULE_URI)
        if not portrules:
            return list(
                {
                    node.value
                    for node in component.find_sources_by_kind(
                        NodeKind.AWS_RECORD_SET_DNS
                    )
                }
            )

        urls = set()
        for portrule_node in portrules:
            for node in portrule_node.find_sources_by_kind(NodeKind.AWS_RECORD_SET_DNS):
                if url_matches_dns(portrule_node.value, node.value):
                    urls.add(portrule_node.value)
        return list(urls)

    def _get_component_data(self, component, project):
        if component.value in self._components_cache:
            return self._components_cache[component.value]

        try:
            name = rancher.get_service(project.value, component.value).get("name")
        except requests.RequestException:
            return

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
        datacenters = {}
        for elb_node in component_node.find_sources_by_kind(NodeKind.AWS_ELB_DNS):
            _, zone, _ = elb_node.value.split(".", 2)

            datacenter, _ = models.Datacenter.objects.get_or_create(
                provider=Datacenter.PROVIDER_AWS, region=zone
            )
            service_datacenter, _ = models.ServiceDatacenter.objects.get_or_create(
                service=service, datacenter=datacenter
            )
            datacenters.setdefault(service_datacenter.id, service_datacenter)
        return datacenters.values()

    @transaction.atomic
    def link_image_to_service(self, image_node, service):
        datacenters_components = defaultdict(set)

        for component in image_node.find_sources_by_kind(NodeKind.RANCHER_SERVICE_ID):
            datacenters = self._get_amazon_datacenters(component, service)

            for project in component.find_sources_by_kind(NodeKind.RANCHER_PROJ_ID):
                component_data = self._get_component_data(component, project)
                project_members = self._get_project_members(project)

                for service_datacenter in datacenters:
                    self._create_component(service_datacenter, component_data)

                    if component_data:
                        # save service_datacenter with components for later deletion
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
