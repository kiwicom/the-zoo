from django.db import transaction

from .models import InfraNode, NodeKind
from .utils import GCPClient, KubernetesClient

CLUSTER_IDENTIFIER = "gke_{project_id}_{zone}_{name}"


def _workload_identifier(cluster, resource_type, resource):
    return f"{cluster}:{resource_type}:{resource.metadata.namespace}/{resource.metadata.name}"


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
        project_node = InfraNode.get_or_create_node(
            kind=NodeKind.GCP_PROJ_ID, value=project["projectId"], source=root
        )

        # currently not used anywhere
        for ip_rule in gcloud.get_forwarding_rules(project["projectId"]):
            if ip_rule["loadBalancingScheme"] == "EXTERNAL":
                InfraNode.get_or_create_node(
                    kind=NodeKind.GCP_IP_RULE_NAME,
                    value=f"{ip_rule['id']}:{ip_rule['IPAddress']}:{ip_rule['portRange']}",
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

            for resource_type, resources in workloads.items():
                for resource in resources:
                    workload_node = InfraNode.get_or_create_node(
                        kind=NodeKind.GCP_WORKLOAD_NAME,
                        value=_workload_identifier(
                            cluster_ctx, resource_type, resource
                        ),
                        source=cluster_node,
                    )

                    for container in resource.spec.template.spec.containers:
                        InfraNode.get_or_create_node(
                            kind=NodeKind.DOCKER_IMAGE_UUID,
                            value=container.image,
                            source=workload_node,
                        )
