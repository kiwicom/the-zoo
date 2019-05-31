import itertools
import pathlib

import boto3
from django.conf import settings
from django.db import transaction

from .models import InfraNode, NodeKind

config_file = pathlib.Path(settings.AWS_CONFIG_FILE)
credentials_file = pathlib.Path(settings.AWS_CREDENTIALS_FILE)

if settings.AWS_CONFIG and not config_file.is_file():
    config_file.parents[0].mkdir(parents=True, exist_ok=True)
    config_file.write_text(settings.AWS_CONFIG)

if settings.AWS_CREDENTIALS and not credentials_file.is_file():
    credentials_file.parents[0].mkdir(parents=True, exist_ok=True)
    credentials_file.write_text(settings.AWS_CREDENTIALS)


def _get_url(value):
    if value.startswith("dualstack."):
        value = value[10:]
    return value.strip().rstrip(".").replace("\\052", "*")


def get_client(service_name, profile_name="default"):
    return boto3.Session(profile_name=profile_name).client(service_name)


def get_profiles(name="*"):
    if "*" not in name:
        return [name]

    available = boto3.Session().available_profiles
    selected = []

    for profile in available:
        prefix, suffix = name.split("*")
        if profile.startswith(prefix) and profile.endswith(suffix):
            selected.append(profile)

    return selected


def iter_hosted_zones(profile_name="default"):
    route53 = get_client("route53", profile_name)
    paginator = route53.get_paginator("list_hosted_zones")

    for page in paginator.paginate():
        yield from page["HostedZones"]


def iter_resource_record_sets(hosted_zones_ids, profile_name="default"):
    route53 = get_client("route53", profile_name)
    for zone_id in hosted_zones_ids:
        paginator = route53.get_paginator("list_resource_record_sets")

        for page in paginator.paginate(HostedZoneId=zone_id):
            yield from page["ResourceRecordSets"]


def iter_load_balancers(names=None, profile_name="default", version=1):
    if version == 1:
        client = get_client("elb", profile_name)
    elif version == 2:
        client = get_client("elbv2", profile_name)
    else:
        raise ValueError(f"Unsupported version: {version}")

    paginator = client.get_paginator("describe_load_balancers")

    if names:
        page_iterator = paginator.paginate(LoadBalancerArns=names)
    else:
        page_iterator = paginator.paginate()

    for page in page_iterator:
        if version == 1:
            yield from page["LoadBalancerDescriptions"]
        else:
            yield from page["LoadBalancers"]


def iter_ec2_instances(instance_ids=None, profile_name="default"):
    ec2 = get_client("ec2", profile_name)
    paginator = ec2.get_paginator("describe_instances")

    if instance_ids:
        page_iterator = paginator.paginate(InstanceIds=instance_ids)
    else:
        page_iterator = paginator.paginate()

    for page in page_iterator:
        for reservations in page["Reservations"]:
            yield from reservations["Instances"]


@transaction.atomic
def _map_dns_records(profile_name="default"):
    """Map DNS records (from Amazon Route 53) to the database as a set of InfraNodes.

    Creates records in the InfraNode table of the following kinds:

    - ``aws.root.dns`` - root of all Amazon DNS records
    - ``aws.hostedzone.dns`` - results from Route 53 > ListHostedZones
    - ``aws.recordset.dns`` - results from Route 53 > ListResourceRecordSets
    """
    root = InfraNode.get_or_create_node(kind=NodeKind.AWS_ROOT_DNS, value="*")

    for zone in iter_hosted_zones(profile_name=profile_name):
        zone_path = InfraNode.get_or_create_node(
            kind=NodeKind.AWS_HOSTED_ZONE_DNS, value=_get_url(zone["Name"]), source=root
        )

        if "AliasTarget" in zone and zone["AliasTarget"].get("DNSName"):
            InfraNode.get_or_create_node(
                kind=NodeKind.AWS_RECORD_SET_DNS,
                value=_get_url(zone["AliasTarget"]["DNSName"]),
                source=zone_path,
            )

        record_sets = iter_resource_record_sets([zone["Id"]], profile_name=profile_name)

        for record_set in record_sets:
            record_set_path = InfraNode.get_or_create_node(
                kind=NodeKind.AWS_RECORD_SET_DNS,
                value=_get_url(record_set["Name"]),
                source=zone_path,
            )

            record_type = record_set.get("Type")

            if record_type == "CNAME":
                value = record_set["ResourceRecords"][0]["Value"]
            elif record_type == "A" and "AliasTarget" in record_set:
                value = record_set["AliasTarget"]["DNSName"]
            else:
                continue

            if value:
                InfraNode.get_or_create_node(
                    kind=NodeKind.AWS_RECORD_SET_DNS,
                    value=_get_url(value),
                    source=record_set_path,
                )


@transaction.atomic
def _map_dns_to_ec2s(profile_name="default"):
    """Map all DNS records found in the ``InfraNode`` table via ELBs to EC2 instances.

    Creates records in the InfraNode table of the following kinds:

    - ``aws.elb.dns`` - Public DNS of an Elastic Load Balancer (ELB and ELBv2)
    - ``aws.ec2.dns.private`` - Private DNS of an EC2 instance
    """
    record_set_nodes = InfraNode.objects.filter(kind=NodeKind.AWS_RECORD_SET_DNS).all()

    load_balancers = {
        _get_url(elb["DNSName"]): elb
        for elb in itertools.chain(
            iter_load_balancers(profile_name=profile_name),
            iter_load_balancers(profile_name=profile_name, version=2),
        )
    }
    ec2_instances = {
        ec2["InstanceId"]: ec2 for ec2 in iter_ec2_instances(profile_name=profile_name)
    }

    for record_set_node in record_set_nodes:
        elb_info = load_balancers.get(record_set_node.value)

        if elb_info is None:
            continue

        elb_node = InfraNode.get_or_create_node(
            kind=NodeKind.AWS_ELB_DNS,
            value=_get_url(elb_info["DNSName"]),
            source=record_set_node,
        )

        for instance_info in elb_info.get("Instances", []):
            instance = ec2_instances[instance_info["InstanceId"]]
            InfraNode.get_or_create_node(
                kind=NodeKind.AWS_EC2_DNS_PRIVATE,
                value=instance["PrivateDnsName"],
                source=elb_node,
            )


def map_to_nodes(profiles="*"):
    """Map Amazon infrastructure to a set of ``InfraNode``s."""
    for profile_name in get_profiles(name=profiles):
        _map_dns_records(profile_name=profile_name)
        _map_dns_to_ec2s(profile_name=profile_name)
