import pytest
from faker import Faker

from zoo.datacenters import amazon as uut
from zoo.datacenters import models

fake = Faker()
pytestmark = pytest.mark.django_db


def test_amazon_map_to_nodes(mocker):
    mocker.patch(
        "zoo.datacenters.amazon.iter_hosted_zones",
        return_value=[
            {"Id": "hostedzone/1", "Name": "example.com"},
            {
                "Id": "hostedzone/2",
                "Name": "zoo.example.com",
                "AliasTarget": {"DNSName": "elb1.example.com"},
            },
        ],
    )
    mocker.patch(
        "zoo.datacenters.amazon.iter_resource_record_sets",
        return_value=[
            {
                "Type": "A",
                "Name": "test.example.com",
                "AliasTarget": {"DNSName": "elb1.example.com"},
            },
            {
                "Type": "CNAME",
                "Name": "test2.example.com",
                "ResourceRecords": [{"Value": "elb2.example.com"}],
            },
        ],
    )

    def get_load_balancers(version=1, **kwargs):
        result = None
        if version == 1:
            result = [
                {
                    "DNSName": "elb1.example.com",
                    "Instances": [{"InstanceId": "i-a"}, {"InstanceId": "i-b"}],
                }
            ]
        elif version == 2:
            result = [
                {"DNSName": "elb2.example.com", "Instances": [{"InstanceId": "i-c"}]}
            ]
        return result

    mocker.patch("zoo.datacenters.amazon.iter_load_balancers", new=get_load_balancers)
    mocker.patch(
        "zoo.datacenters.amazon.iter_ec2_instances",
        return_value=[
            {"InstanceId": "i-a", "PrivateDnsName": "ip-1"},
            {"InstanceId": "i-b", "PrivateDnsName": "ip-2"},
            {"InstanceId": "i-c", "PrivateDnsName": "ip-3"},
        ],
    )

    uut.map_to_nodes(profiles="default")

    root = models.InfraNode.objects.get(kind=models.NodeKind.AWS_ROOT_DNS)

    zones = {zone.value: zone for zone in root.targets.all()}
    assert set(zones) == {"zoo.example.com", "example.com"}

    record_sets = {rs.value: rs for rs in zones["example.com"].targets.all()}
    assert set(record_sets) == {"test.example.com", "test2.example.com"}

    [elb1_dns] = record_sets["test.example.com"].targets.all()
    [elb2_dns] = record_sets["test2.example.com"].targets.all()

    [elb1] = elb1_dns.targets.all()
    [elb2] = elb2_dns.targets.all()

    assert elb1.value == "elb1.example.com"
    assert elb2.value == "elb2.example.com"

    assert {instance.value for instance in elb1.targets.all()} == {"ip-1", "ip-2"}
    assert {instance.value for instance in elb2.targets.all()} == {"ip-3"}
