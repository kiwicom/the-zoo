def get_datacenter_template_data(service_datacenter):
    datacenter = service_datacenter.datacenter
    provider = datacenter.provider

    component_labels = {}
    members_labels = {}
    provider_icons = {
        datacenter.PROVIDER_GCP: "cog",
        datacenter.PROVIDER_AWS: "cog",
    }
    platform = {
        datacenter.PROVIDER_GCP: "kubernetes",
        datacenter.PROVIDER_AWS: "rancher",
    }

    return {
        "provider": provider,
        "provider_icon": provider_icons.get(provider, "server"),
        "platform": platform.get(provider, provider),
        "region": datacenter.region,
        "components": service_datacenter.components.all(),
        "components_label": component_labels.get(provider, "Components"),
        "members": service_datacenter.members.all(),
        "members_label": members_labels.get(provider, "Members"),
    }
