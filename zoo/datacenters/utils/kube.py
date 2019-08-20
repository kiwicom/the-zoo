from base64 import decodebytes
from tempfile import NamedTemporaryFile

import googleapiclient
from kubernetes import client

from . import gcloud

BLACKLISTED_NAMESPACES = ["kube-system", "kube-public", "system"]


class KubernetesClient:
    def __init__(self, cluster):
        config = client.Configuration()
        config.host = f"https://{cluster['endpoint']}"

        config.api_key_prefix["authorization"] = "Bearer"
        config.api_key["authorization"] = _token(
            gcloud._get_credentials(), "cloud-platform"
        )

        with NamedTemporaryFile(delete=False) as cert:
            cert.write(
                decodebytes(cluster["masterAuth"]["clusterCaCertificate"].encode())
            )
            config.ssl_ca_cert = cert.name

        self.client = client.ApiClient(configuration=config)

    def iter_workloads(self):
        def _filter_resources(resources):
            return [
                resource
                for resource in resources
                if resource.metadata.namespace not in BLACKLISTED_NAMESPACES
            ]

        apps = client.AppsV1Api(self.client)
        batch = client.BatchV1Api(self.client)
        batch_v1_beta = client.BatchV1beta1Api(self.client)

        workloads = {
            "deployments": _filter_resources(
                apps.list_deployment_for_all_namespaces().items
            ),
            "statefulsets": _filter_resources(
                apps.list_stateful_set_for_all_namespaces().items
            ),
            "daemonsets": _filter_resources(
                apps.list_daemon_set_for_all_namespaces().items
            ),
            "jobs": _filter_resources(batch.list_job_for_all_namespaces().items),
            "cronjobs": _filter_resources(
                batch_v1_beta.list_cron_job_for_all_namespaces().items
            ),
        }

        return workloads

    def get_ingress(self, namespace):
        try:
            ingresses = (
                client.NetworkingV1beta1Api(self.client)
                .list_namespaced_ingress(namespace)
                .items
            )
        except client.rest.ApiException:
            ingresses = (
                client.ExtensionsV1beta1Api(self.client)
                .list_namespaced_ingress(namespace)
                .items
            )

        return ingresses


def _token(credentials, *scopes):
    scopes = [f"https://www.googleapis.com/auth/{s}" for s in scopes]
    scoped = googleapiclient._auth.with_scopes(credentials, scopes)
    googleapiclient._auth.refresh_credentials(scoped)

    return scoped.token
