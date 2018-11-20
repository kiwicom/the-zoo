from collections import defaultdict
from enum import Enum
import importlib
from pathlib import Path
import pkgutil
import re
import site
from typing import Dict

import attr
from django.conf import settings
import yaml

CHECK_REGEX = r"^check\w*"

KINDS = {}
CHECKS = []


class Severity(Enum):
    UNDEFINED = "undefined"
    ADVICE = "advice"
    WARNING = "warning"
    CRITICAL = "critical"


class Effort(Enum):
    UNDEFINED = "undefined"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@attr.s(frozen=True, slots=True)
class Kind:

    namespace = attr.ib()
    category = attr.ib(cmp=False, repr=False)
    id = attr.ib()
    title = attr.ib(cmp=False, repr=False)
    description = attr.ib(cmp=False, repr=False)
    severity = attr.ib(
        cmp=False,
        repr=False,
        default=Severity.UNDEFINED,
        validator=attr.validators.instance_of(Severity),
        converter=Severity,
    )
    effort = attr.ib(
        cmp=False,
        repr=False,
        default=Effort.UNDEFINED,
        validator=attr.validators.instance_of(Effort),
        converter=Effort,
    )

    @property
    def key(self):
        return f"{self.namespace}:{self.id}"

    def format_description(self, details):
        return self.description.format_map(defaultdict(str, details or {}))


class IncorrectCheckMetadataError(Exception):
    pass


def _parse_metadata_file(package_path: Path, module_name: str) -> Dict:
    with (package_path / "metadata" / f"{module_name}.yml").open() as metadata_file:
        try:
            header, details = yaml.safe_load_all(metadata_file)
            return {
                kind.key: kind for kind in [Kind(**header, **data) for data in details]
            }
        except (ValueError, KeyError) as exc:
            raise IncorrectCheckMetadataError("File format not correct") from exc


def raise_package_exception(name):
    print(name)


def clear_discovered_checks():
    KINDS.clear()
    CHECKS.clear()


def discover_checks():
    clear_discovered_checks()

    if not settings.ZOO_AUDITING_CHECKS:
        return

    site.addsitedir(str(settings.ZOO_AUDITING_ROOT))

    for package_name in settings.ZOO_AUDITING_CHECKS:
        package = importlib.import_module(f"{package_name}.checks")

        for _, module_full_name, ispkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + ".",
            onerror=raise_package_exception,
        ):
            if not ispkg:
                module_name = module_full_name.rsplit(".", 1)[1]
                if re.match(CHECK_REGEX, module_name):
                    module = importlib.import_module(module_full_name)

                    KINDS.update(
                        _parse_metadata_file(
                            settings.ZOO_AUDITING_ROOT / package_name, module_name
                        )
                    )

                    CHECKS.extend(
                        [
                            getattr(module, member)
                            for member in dir(module)
                            if re.match(CHECK_REGEX, member)
                            and callable(getattr(module, member))
                        ]
                    )


discover_checks()
