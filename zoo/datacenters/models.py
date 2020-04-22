import arrow
from django.contrib.postgres import fields as pg_fields
from django.db import models


def utcnow():
    return arrow.utcnow().datetime


class NodeKind:
    AWS_ROOT_DNS = "aws.root.dns"
    AWS_HOSTED_ZONE_DNS = "aws.hostedzone.dns"
    AWS_RECORD_SET_DNS = "aws.recordset.dns"
    AWS_ELB_DNS = "aws.elb.dns"
    AWS_EC2_DNS_PRIVATE = "aws.ec2.dns.private"

    RANCHER_ROOT_PROJ = "rancher.root.proj"
    RANCHER_PROJ_ID = "rancher.proj.id"
    RANCHER_HOST_DNS = "rancher.host.dns"
    RANCHER_LB_ID = "rancher.lb.id"
    RANCHER_LB_PORTRULE_URI = "rancher.lb.portrule.uri"
    RANCHER_SERVICE_ID = "rancher.service.id"

    GCP_ROOT_PROJ = "gcp.root.proj"
    GCP_PROJ_ID = "gcp.project.id"
    GCP_IP_RULE_NAME = "gcp.ip_rule.name"
    GCP_CLUSTER_NAME = "gcp.cluster.name"
    GCP_WORKLOAD_NAME = "gcp.workload.name"

    DOCKER_IMAGE_UUID = "docker.image.uuid"


class InfraNode(models.Model):
    sources = models.ManyToManyField(
        "InfraNode", related_name="targets", related_query_name="target"
    )
    value = models.CharField(max_length=500)
    kind = models.CharField(max_length=50)
    checked_at = models.DateTimeField(default=utcnow)

    class Meta:
        unique_together = ["value", "kind"]

    def pretty_str(self, separator=""):
        result = f"{separator} ({self.kind}) {self.value}\n"
        for target in self.targets.order_by("value").all():
            result += target.pretty_str(separator=separator + "   ")
        return result

    def find_sources_by_kind(self, kind):
        sources = list(self.sources.all())
        sources_of_kind = []
        visited = set()

        while sources:
            source = sources.pop()
            if source.id in visited:
                continue
            visited.add(source.id)
            if source.kind == kind:
                sources_of_kind.append(source)
            sources.extend(source.sources.all())

        return sources_of_kind

    @classmethod
    def get_or_create_node(cls, kind, value, source=None):
        node, _ = cls.objects.get_or_create(kind=kind, value=value)
        if source is not None:
            node.sources.add(source)
        node.checked_at = utcnow()
        node.save(update_fields=["checked_at"])
        return node


class Datacenter(models.Model):
    PROVIDER_GCP = "GCP"
    PROVIDER_AWS = "AWS"

    provider = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("provider", "region")

    def __str__(self):
        return f"{self.provider} {self.region}" if self.region else self.provider


class ServiceDatacenter(models.Model):
    service = models.ForeignKey(
        "services.Service", on_delete=models.CASCADE, related_name="datacenters"
    )
    datacenter = models.ForeignKey("Datacenter", on_delete=models.PROTECT)

    class Meta:
        unique_together = ("service", "datacenter")


class ServiceDatacenterMember(models.Model):
    service_datacenter = models.ForeignKey(
        "ServiceDatacenter",
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="member",
    )
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    class Meta:
        unique_together = ["service_datacenter", "name"]


class ServiceDatacenterComponent(models.Model):
    service_datacenter = models.ForeignKey(
        "ServiceDatacenter",
        on_delete=models.CASCADE,
        related_name="components",
        related_query_name="component",
    )
    name = models.CharField(max_length=100)
    urls = pg_fields.ArrayField(
        base_field=models.URLField(max_length=500), blank=True, default=list
    )

    class Meta:
        unique_together = ["service_datacenter", "name"]
