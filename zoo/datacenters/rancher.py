from urllib.parse import urljoin

from django.conf import settings
from django.db import transaction

from ..base.http import session
from .models import InfraNode, NodeKind


def get(path, params=None):
    url = urljoin(settings.RANCHER_API_URL, path)
    auth = (settings.RANCHER_ACCESS_KEY, settings.RANCHER_SECRET_KEY)

    resp = session.get(url, auth=auth, params=params)
    resp.raise_for_status()
    return resp.json()


def iter_get(path):
    content = get(path)

    while content.get("data"):
        yield from content["data"]
        next_page_url = (content.get("pagination") or {}).get("next")

        if next_page_url is None:
            break
        content = get(next_page_url)


def iter_projects():
    yield from iter_get("projects")


def get_project(project_id):
    return get(f"projects/{project_id}")


def iter_services(project_id):
    yield from iter_get(f"projects/{project_id}/services/")


def get_service(project_id, service_id):
    return get(f"projects/{project_id}/services/{service_id}")


def iter_load_balancers(project_id):
    yield from iter_get(f"projects/{project_id}/loadbalancerservices/")


def iter_hosts(project_id):
    yield from iter_get(f"projects/{project_id}/hosts/")


def parse_members_from_project(project_data):
    members = []
    for member in project_data["members"]:
        external_id = member.get("externalId")
        if external_id is None:
            continue

        data = dict(item.split("=", 1) for item in external_id.split(","))
        members.append(data.get("cn"))
    return members


def _map_lb_to_services(lb, hosts, project_node):
    lb_node = InfraNode.get_or_create_node(kind=NodeKind.RANCHER_LB_ID, value=lb["id"])
    for endpoint in lb["publicEndpoints"]:
        host_node = InfraNode.get_or_create_node(
            kind=NodeKind.RANCHER_HOST_DNS,
            value=hosts[endpoint["hostId"]],
            source=project_node,
        )
        lb_node.sources.add(host_node)

    service_nodes = []
    for rule in lb.get("lbConfig", {}).get("portRules", []):
        if not rule["protocol"].startswith("http"):
            continue

        uri = (
            rule["hostname"]
            if rule["sourcePort"] == 80
            else f"{rule['hostname']}:{rule['sourcePort']}"
        )
        portrule_node = InfraNode.get_or_create_node(
            kind=NodeKind.RANCHER_LB_PORTRULE_URI, value=uri, source=lb_node
        )
        service_node = InfraNode.get_or_create_node(
            kind=NodeKind.RANCHER_SERVICE_ID,
            value=rule["serviceId"],
            source=portrule_node,
        )
        service_nodes.append(service_node)

    return service_nodes


@transaction.atomic
def map_to_nodes():
    """Map Rancher projects (i.e. Rancher environments) to Rancher services.

    Creates records in the InfraNode table of the following kinds:

    - ``rancher.root.proj`` - root node for all Rancher projects
    - ``rancher.proj.id`` - Rancher project ID
    - ``rancher.host.dns`` - Rancher host's DNS
    - ``rancher.lb.id`` - Rancher load balancer service's ID
    - ``rancher.lb.portrule.uri`` - Port rule of a Rancher load balancer service
    - ``rancher.service.id`` - Rancher service ID
    - ``docker.image.uuid`` - Docker image UUID
    """
    root = InfraNode.get_or_create_node(kind=NodeKind.RANCHER_ROOT_PROJ, value="*")

    for project in iter_projects():
        project_node = InfraNode.get_or_create_node(
            kind=NodeKind.RANCHER_PROJ_ID, value=project["id"], source=root
        )
        hosts = {
            host["id"]: host["hostname"]
            for host in iter_hosts(project_id=project["id"])
        }
        services = {
            service["id"]: service["launchConfig"]["imageUuid"]
            for service in iter_services(project_id=project["id"])
            if service.get("launchConfig", {}).get("imageUuid")
        }

        all_service_nodes = []

        for lb in iter_load_balancers(project_id=project["id"]):
            all_service_nodes += _map_lb_to_services(lb, hosts, project_node)

        for service_node in all_service_nodes:
            InfraNode.get_or_create_node(
                kind=NodeKind.DOCKER_IMAGE_UUID,
                value=services[service_node.value],
                source=service_node,
            )
