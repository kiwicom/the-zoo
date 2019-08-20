from django.db import transaction
import googleapiclient

from .models import InfraNode, NodeKind
from .utils import GCPClient, KubernetesClient

CLUSTER_IDENTIFIER = "gke_{project_id}_{zone}_{name}"


def _workload_identifier(cluster, resource_type, resource):
    return f"{cluster}:{resource_type}:{resource.metadata.namespace}/{resource.metadata.name}"


def _map_workloads(workloads, cluster_ctx, cluster_node):
    for resource_type, resources in workloads.items():
        for resource in resources:
            workload_node = InfraNode.get_or_create_node(
                kind=NodeKind.GCP_WORKLOAD_NAME,
                value=_workload_identifier(cluster_ctx, resource_type, resource),
                source=cluster_node,
            )

            if resource_type == "cronjobs":
                containers = resource.spec.job_template.spec.template.spec.containers
            else:
                containers = resource.spec.template.spec.containers

            for container in containers:
                InfraNode.get_or_create_node(
                    kind=NodeKind.DOCKER_IMAGE_UUID,
                    value=container.image,
                    source=workload_node,
                )


@transaction.atomic
def map_to_nodes():
    """Map GCP projects to GCP services.

    Creates records in the InfraNode table of the following kinds:

    - ``gcp.root.proj`` - root node for all GCP projects
    - ``gcp.proj.id`` - GCP project ID
    - ``gcp.ip_rule.name`` - GCP forwarding rule name
    - ``gcp.cluster.name`` - GCP cluster name
    - ``gcp.workload.name`` - GCP workload name (including the namespace)
    - ``docker.image.uuid`` - Docker image UUID
    """
    root = InfraNode.get_or_create_node(kind=NodeKind.GCP_ROOT_PROJ, value="*")
    gcloud = GCPClient()

    for project in gcloud.get_all_projects():
        if project["projectId"].startswith("sys-"):
            # skip "shadow" projects
            # see https://skypicker.slack.com/archives/C1XN8EPAP/p1568641244031000
            continue

        project_node = InfraNode.get_or_create_node(
            kind=NodeKind.GCP_PROJ_ID, value=project["projectId"], source=root
        )

        try:
            # skip projects without billing enabled
            ip_rules = list(gcloud.get_forwarding_rules(project["projectId"]))
        except googleapiclient.errors.HttpError:
            continue

        # currently not used anywhere
        for ip_rule in ip_rules:
            port_range = f":{ip_rule['portRange']}" if "portRange" in ip_rule else ""
            if ip_rule["loadBalancingScheme"] == "EXTERNAL":
                InfraNode.get_or_create_node(
                    kind=NodeKind.GCP_IP_RULE_NAME,
                    value=f"{ip_rule['id']}:{ip_rule['IPAddress']}{port_range}",
                    source=project_node,
                )

        for cluster in gcloud.get_all_clusters(project["projectId"]):
            cluster_ctx = CLUSTER_IDENTIFIER.format(
                project_id=project["projectId"],
                zone=cluster["zone"],
                name=cluster["name"],
            )
            cluster_node = InfraNode.get_or_create_node(
                kind=NodeKind.GCP_CLUSTER_NAME, value=cluster_ctx, source=project_node
            )

            kube = KubernetesClient(cluster)
            workloads = kube.iter_workloads()

            _map_workloads(workloads, cluster_ctx, cluster_node)
