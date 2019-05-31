import pytest

from zoo.datacenters import models as uut

pytestmark = pytest.mark.django_db


def test_infra_node__get_or_create_node():
    root = uut.InfraNode.get_or_create_node(kind="kind1", value="value1")

    assert root.value == "value1"
    assert list(root.sources.all()) == []
    assert list(root.targets.all()) == []

    node = uut.InfraNode.get_or_create_node(kind="kind2", value="value2", source=root)

    assert list(node.sources.all()) == [root]
    assert list(root.targets.all()) == [node]

    assert root.id == uut.InfraNode.get_or_create_node(kind="kind1", value="value1").id


def test_infra_node__find_sources_by_kind():
    root = uut.InfraNode.objects.create(kind="root", value="123")

    node_dns = uut.InfraNode.objects.create(kind="dns", value="a1b")
    node_abc = uut.InfraNode.objects.create(kind="abc", value="a2b")

    root.targets.add(node_dns)
    root.targets.add(node_abc)

    node_dns2 = uut.InfraNode.objects.create(kind="dns", value="b11")
    node_dns3 = uut.InfraNode.objects.create(kind="dns", value="b22")
    node_abc.targets.add(node_dns2)
    node_dns2.targets.add(node_dns3)

    leaf = uut.InfraNode.objects.create(kind="leaf", value="ccc")
    node_dns.targets.add(leaf)
    node_dns3.targets.add(leaf)

    dns_sources = leaf.find_sources_by_kind("dns")
    dns_nodes_ids = {node_dns.id, node_dns2.id, node_dns3.id}
    assert {source.id for source in dns_sources} == dns_nodes_ids

    root_sources = leaf.find_sources_by_kind("root")
    assert list(root_sources) == [root]
