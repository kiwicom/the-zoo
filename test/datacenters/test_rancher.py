import pytest
from faker import Faker

from zoo.datacenters import models
from zoo.datacenters import rancher as uut

fake = Faker()
pytestmark = pytest.mark.django_db


def test_rancher_parse_members_from_project():
    names = [fake.name(), fake.name()]
    members = uut.parse_members_from_project(
        {
            "id": "p2",
            "members": [
                {
                    "type": "projectMember",
                    "externalId": f"cn={names[0]},ou=People,dc=example,dc=com",
                    "role": "owner",
                },
                {
                    "type": "projectMember",
                    "externalId": f"cn={names[1]},ou=People,dc=example,dc=com",
                    "role": "owner",
                },
            ],
        }
    )
    assert members == names


def test_rancher_map_to_nodes(mocker):
    mocker.patch("zoo.datacenters.rancher.iter_projects", return_value=[{"id": "p1"}])
    mocker.patch(
        "zoo.datacenters.rancher.iter_services",
        return_value=[
            {"id": "s1", "launchConfig": {"imageUuid": "docker:lb"}},
            {"id": "s2", "launchConfig": {"imageUuid": "docker:zoo"}},
        ],
    )
    mocker.patch(
        "zoo.datacenters.rancher.iter_load_balancers",
        return_value=[
            {
                "id": "lb1",
                "lbConfig": {
                    "portRules": [
                        {
                            "hostname": "zoo.example.com",
                            "sourcePort": 80,
                            "protocol": "http",
                            "serviceId": "s2",
                        }
                    ]
                },
                "publicEndpoints": [{"hostId": "h1"}],
            }
        ],
    )
    mocker.patch(
        "zoo.datacenters.rancher.iter_hosts",
        return_value=[{"id": "h1", "hostname": "ip-127-0-0-1"}],
    )

    uut.map_to_nodes()

    project = models.InfraNode.objects.get(kind=models.NodeKind.RANCHER_PROJ_ID)
    assert project.value == "p1"

    hosts = project.targets.all()
    assert {host.value for host in hosts} == {"ip-127-0-0-1"}

    lbs = hosts[0].targets.all()
    assert {lb.value for lb in lbs} == {"lb1"}

    portrules = lbs[0].targets.all()
    assert {portrule.value for portrule in portrules} == {"zoo.example.com"}

    services = portrules[0].targets.all()
    assert {service.value for service in services} == {"s2"}

    images = services[0].targets.all()
    assert {image.value for image in images} == {"docker:zoo"}
