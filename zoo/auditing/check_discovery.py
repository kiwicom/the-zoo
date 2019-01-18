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
    patch = attr.ib(default=None, cmp=False, repr=False)
    description = attr.ib(default="", cmp=False, repr=False)
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

    @property
    def apply_patch(self):
        if self.patch is None:
            return
        return PATCHES.get(self.key)

    def format_description(self, details):
        return self.description.format_map(defaultdict(str, details or {}))


CHECK_REGEX = r"^check\w*"
PATCH_REGEX = r"^patch\w*"

KINDS = defaultdict(
    lambda: Kind(
        id="deleted",
        patch="deleted",
        namespace="deleted",
        category="deleted",
        title="[deleted issue]",
        description="This issue has been deleted so there is no description available for it.",
    )
)
CHECKS = []
PATCHES = {}


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
    PATCHES.clear()


def discover_checks():
    clear_discovered_checks()

    if not settings.ZOO_AUDITING_CHECKS:
        return

    site.addsitedir(str(settings.ZOO_AUDITING_ROOT))

    for package_name in settings.ZOO_AUDITING_CHECKS:
        package = importlib.import_module(f"{package_name}.checks")
        package_kinds = {}

        for module_name, module in _get_package_members(package, CHECK_REGEX):
            CHECKS.extend(
                [member for _, member in _get_module_members(module, CHECK_REGEX)]
            )
            package_kinds.update(
                _parse_metadata_file(
                    settings.ZOO_AUDITING_ROOT / package_name, module_name
                )
            )

        KINDS.update(package_kinds)

        try:
            package = importlib.import_module(f"{package_name}.patches")
        except ModuleNotFoundError:
            continue

        patches_keys = {
            kind.patch: kind.key
            for kind in package_kinds.values()
            if kind.patch is not None
        }

        for module_name, module in _get_package_members(package, PATCH_REGEX):
            PATCHES.update(
                {
                    patches_keys[f"{module_name}.{member_name}"]: member
                    for member_name, member in _get_module_members(module, PATCH_REGEX)
                }
            )


def _get_package_members(package, filter_by_re=None):
    for _, module_full_name, ispkg in pkgutil.walk_packages(
        path=package.__path__,
        prefix=package.__name__ + ".",
        onerror=raise_package_exception,
    ):
        if not ispkg:
            module_name = module_full_name.rsplit(".", 1)[1]
            if filter_by_re is not None and re.match(filter_by_re, module_name):
                module = importlib.import_module(module_full_name)
                yield module_name, module


def _get_module_members(module, filter_by_re=None):
    return (
        (member_name, getattr(module, member_name))
        for member_name in dir(module)
        if (filter_by_re is None or re.match(filter_by_re, member_name))
        and callable(getattr(module, member_name))
    )


discover_checks()
