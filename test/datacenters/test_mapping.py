from zoo.datacenters import mapping as uut


def test_url_matches_dns():
    assert uut.url_matches_dns("zoo.example.com", "*.example.com")
    assert uut.url_matches_dns("zoo.example.com", "zoo.*.com")
    assert uut.url_matches_dns("zoo.example.com", "zoo.example.com")

    assert not uut.url_matches_dns("zoo.example.com", "abc.example.com")
    assert not uut.url_matches_dns("zoo.example.com", "abc.*.com")
    assert not uut.url_matches_dns("zoo.example.com", "*.example.cz")
