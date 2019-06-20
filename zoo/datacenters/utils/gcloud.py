from django.conf import settings
from google.oauth2 import service_account
from googleapiclient import discovery


def _get_credentials():
    if settings.GCP_SERVICE_KEY is None:
        raise RuntimeError("gcloud auth couldn't be performed, missing env variable")

    return service_account.Credentials.from_service_account_info(
        settings.GCP_SERVICE_KEY
    )


class GCPClient:
    def __init__(self):
        self.credentials = _get_credentials()

        self.projectService = discovery.build(
            "cloudresourcemanager", "v1", credentials=self.credentials
        )
        self.computeService = discovery.build(
            "compute", "v1", credentials=self.credentials
        )
        self.containerService = discovery.build(
            "container", "v1", credentials=self.credentials
        )

    def get_all_projects(self):
        request = self.projectService.projects().list()
        while request is not None:
            response = request.execute()

            for project in response["projects"]:
                yield project

            request = self.projectService.projects().list_next(
                previous_request=request, previous_response=response
            )

    def get_forwarding_rules(self, project_id):
        request = self.computeService.forwardingRules().aggregatedList(
            project=project_id
        )

        while request is not None:
            response = request.execute()
            for ip_rules in response["items"].values():
                for ip_rule in ip_rules.get("forwardingRules", []):
                    yield ip_rule

            request = self.computeService.forwardingRules().list_next(
                previous_request=request, previous_response=response
            )

    def get_all_clusters(self, project_id):
        clusters = (
            self.containerService.projects()
            .locations()
            .clusters()
            .list(parent="projects/{}/locations/-".format(project_id))
        ).execute()

        # clusters are not a paged resource
        if "clusters" in clusters:
            return clusters["clusters"]

        return []

    def get_project_owners(self, project_id):
        request = self.projectService.projects().getIamPolicy(
            resource=project_id, body={"options": {"requestedPolicyVersion": 0}}
        )
        bindings = request.execute()["bindings"]

        for binding in bindings:
            if binding["role"] == "roles/owner":
                return [
                    member
                    for member in binding["members"]
                    if member.endswith("@kiwi.com")
                ]

    def get_clusters_by_name(self, cluster):
        # zoo.datacenters.gcp.CLUSTER_IDENTIFIER
        _, projectId, zone, name = cluster.split("_")

        return (
            self.containerService.projects()
            .locations()
            .clusters()
            .get(name=f"projects/{projectId}/locations/{zone}/clusters/{name}")
            .execute()
        )
