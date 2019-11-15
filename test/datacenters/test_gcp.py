from unittest.mock import MagicMock

import pytest

from zoo.datacenters import gcp as uut
from zoo.datacenters import models

pytestmark = pytest.mark.django_db


def test_gcp_map_to_nodes(mocker):
    mocker.patch("zoo.datacenters.utils.gcloud.GCPClient.__init__", return_value=None)
    mocker.patch(
        "zoo.datacenters.utils.gcloud.GCPClient.get_all_projects",
        return_value=[{"projectId": "pid1"}, {"projectId": "pid2"}],
    )
    mocker.patch(
        "zoo.datacenters.utils.gcloud.GCPClient.get_forwarding_rules",
        return_value=[
            {
                "id": "test1",
                "loadBalancingScheme": "EXTERNAL",
                "IPAddress": "1.1.1.1",
                "portRange": "443-443",
            },
            {
                "id": "test2",
                "loadBalancingScheme": "INTERNAL",
                "IPAddress": "2.2.2.2",
                "portRange": "443-443",
            },
        ],
    )
    mocker.patch(
        "zoo.datacenters.utils.GCPClient.get_all_clusters",
        return_value=[{"name": "test", "zone": "europe-test"}],
    )
    mocker.patch(
        "zoo.datacenters.utils.kube.KubernetesClient.__init__", return_value=None
    )

    workload = MagicMock()
    image1 = MagicMock()
    image2 = MagicMock()
    image1.image = "test/image:0.0.1"
    image2.image = "test/image2:0.0.2"

    workload.metadata.namespace = "namespace-test"
    workload.metadata.name = "resource-test"
    workload.spec.template.spec.containers = [image1, image2]

    mocker.patch(
        "zoo.datacenters.utils.kube.KubernetesClient.iter_workloads",
        return_value={"test-type": [workload]},
    )

    uut.map_to_nodes()

    root = models.InfraNode.objects.get(kind=models.NodeKind.GCP_ROOT_PROJ)

    projects = {project.value: project for project in root.targets.all()}
    assert set(projects) == {"pid1", "pid2"}

    ctx = "gke_pid1_europe-test_test"
    clusters = {
        cluster.value: cluster
        for cluster in projects["pid1"].targets.filter(
            kind=models.NodeKind.GCP_CLUSTER_NAME
        )
    }
    assert set(clusters) == {ctx}

    ip_rules = {
        cluster.value: cluster
        for cluster in projects["pid1"].targets.filter(
            kind=models.NodeKind.GCP_IP_RULE_NAME
        )
    }
    assert set(ip_rules) == {"test1:1.1.1.1:443-443"}

    workloads = {
        workload.value: workload
        for workload in clusters["gke_pid1_europe-test_test"].targets.all()
    }
    full_name = "test-type:namespace-test/resource-test"
    assert set(workloads) == {f"{ctx}:{full_name}"}

    images = {
        image.value: image for image in workloads[f"{ctx}:{full_name}"].targets.all()
    }
    assert set(images) == {"test/image:0.0.1", "test/image2:0.0.2"}
