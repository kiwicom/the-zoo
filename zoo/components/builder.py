from zoo.components.models import Component, Group


class ComponentBuilder:
    def build_component(self, data):
        if data["spec"]["type"] == "service":
            self._build_service(data)
        elif data["spec"]["spec"] == "library":
            self._build_library(data)
        else:
            self._build_base_component(data)

    def _build_base_component(self, data):
        group = Group.objects.update_or_create(
            product_owner=data["metadata"]["group"]["product_owner"],
            project_owner=data["metadata"]["group"]["project_owner"],
            maintainers=data["metadata"]["group"]["maintainers"],
        )
        Component.objects.update_or_create(
            name=data["metadata"]["name"],
            type=data["metadata"]["type"],
            description=data["metadata"]["description"],
            kind=data["kind"],
            owner=data["metadata"]["owner"],
            tags=data["metadata"]["tags"],
            links="",
        )

    def _build_service(self, data):
        self._build_base_component(data)

    def _build_library(self, data):
        self._build_base_component(data)
