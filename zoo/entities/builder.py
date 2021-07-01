from zoo.entities.models import Entity, Group


class EntityBuilder:
    def entity(self, data):
        if data["kind"] == "component":
            if data["spec"]["type"] == "service":
                self._build_service(data)
            elif data["spec"]["spec"] == "library":
                self._build_library(data)
            else:
                self._build_base_component(data)
        else:
            return NotImplemented

    @staticmethod
    def _build_base_component(data):
        group, _ = Group.objects.update_or_create(
            product_owner=data["metadata"]["group"]["product_owner"],
            project_owner=data["metadata"]["group"]["project_owner"],
            maintainers=data["metadata"]["group"]["maintainers"],
        )
        obj, _ = Entity.objects.update_or_create(
            name=data["metadata"]["name"],
            kind=data["kind"],
            owner=data["metadata"]["owner"],
            type=data["spec"]["type"],
            defaults={
                "group": group,
                "description": data["metadata"]["description"],
                "tags": data["metadata"]["tags"],
                "links": "",
            },
        )
        return obj

    def _build_service(self, data):
        base_component = self._build_base_component(data)

    def _build_library(self, data):
        self._build_base_component(data)
