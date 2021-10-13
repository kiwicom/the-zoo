import structlog
from django.core.management.base import BaseCommand

from zoo.entities.enums import Kind
from zoo.entities.models import Entity, Link
from zoo.libraries.models import Library
from zoo.services.models import Service

log = structlog.get_logger()


class Command(BaseCommand):
    help = "Create entities from services and libraries"

    def handle(self, *args, **options):
        self.service_to_entity()
        self.library_to_entity()

    @staticmethod
    def service_to_entity():
        with open("service_exceptions.csv", "w+") as exceptions:
            exceptions.write(
                "Service name;Service owner;Service repository;Exception\n"
            )
            for service in Service.objects.all():
                if service.repository:
                    log.info("entity.import_services.processing", service=service)
                    try:
                        entity = Entity.objects.create(
                            name=service.name,
                            owner=service.owner,
                            description=service.description,
                            kind=Kind.COMPONENT,
                            type="service",
                            source=service.repository,
                            tags=service.tags,
                            service=service,
                        )

                        if service.docs_url:
                            Link.objects.create(
                                name="Documentation",
                                url=service.docs_url,
                                entity=entity,
                            )

                        if service.slack_channel:
                            Link.objects.create(
                                name="Discussion",
                                url=f"https://app.slack.com/client/T024Z3H2Y/{service.slack_channel}",
                                entity=entity,
                            )
                    except Exception as err:
                        exceptions.write(
                            f"{getattr(service, 'name', '')};{getattr(service, 'owner', '')};{getattr(service, 'repository', '')};{repr((err))}\n"
                        )
                else:
                    exceptions.write(
                        f"{getattr(service, 'name', '')};{getattr(service, 'owner', '')};;Missing repository for service\n"
                    )

    @staticmethod
    def library_to_entity():
        with open("library_exceptions.csv", "w+") as exceptions:
            exceptions.write(
                "Library name;Library owner;Library repository;Exception\n"
            )
            for library in Library.objects.all():
                if library.repository:
                    log.info("entity.import_libraries.processing", library=library)
                    try:
                        entity = Entity.objects.create(
                            name=library.name,
                            owner=library.owner,
                            description=library.description,
                            kind=Kind.COMPONENT,
                            type="library",
                            source=library.repository,
                            tags=library.tags,
                            library=library,
                        )

                        if library.docs_url:
                            Link.objects.create(
                                name="Documentation",
                                url=library.docs_url,
                                entity=entity,
                            )

                        if library.slack_channel:
                            Link.objects.create(
                                name="Discussion",
                                url=f"https://app.slack.com/client/T024Z3H2Y/{library.slack_channel}",
                                entity=entity,
                            )

                        if library.library_url:
                            Link.objects.create(
                                name="Library URL",
                                url=library.library_url,
                                entity=entity,
                            )
                    except Exception as err:
                        exceptions.write(
                            f"{getattr(library, 'name', '')};{getattr(library, 'owner', '')};{getattr(library, 'repository', '')};{repr((err))}\n"
                        )
                else:
                    exceptions.write(
                        f"{getattr(library, 'name', '')};{getattr(library, 'owner', '')};;Missing repository for library\n"
                    )
