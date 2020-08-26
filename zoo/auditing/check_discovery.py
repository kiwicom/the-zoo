import importlib
import pkgutil
import re
import site
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Dict

import attr
import structlog
import yaml
from django.conf import settings

log = structlog.get_logger()


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
class Kind:  # pylint: disable=too-many-instance-attributes

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


def log_error(name):
    log.info("auditing.check_discovery.scan.fail", name=name)


def clear_discovered_checks():
    KINDS.clear()
    CHECKS.clear()
    PATCHES.clear()


def _discover_kinds(package_name):
    package = importlib.import_module(f"{package_name}.checks")
    package_kinds = {}

    for module_name, module in _get_package_members(package, CHECK_REGEX):
        CHECKS.extend(
            [member for _, member in _get_module_members(module, CHECK_REGEX)]
        )
        package_kinds.update(
            _parse_metadata_file(settings.ZOO_AUDITING_ROOT / package_name, module_name)
        )
    return package_kinds


def _discover_patches(package_name, package_kinds):
    try:
        package = importlib.import_module(f"{package_name}.patches")
    except ModuleNotFoundError:
        return {}

    patches_keys = defaultdict(list)
    for kind in package_kinds.values():
        if kind.patch is None:
            continue
        patches_keys[kind.patch].append(kind.key)

    package_patches = {}
    for module_name, module in _get_package_members(package, PATCH_REGEX):
        for member_name, member in _get_module_members(module, PATCH_REGEX):
            patch_key = f"{module_name}.{member_name}"
            for kind_key in patches_keys.get(patch_key, []):
                package_patches[kind_key] = member

    return package_patches


def discover_checks():
    clear_discovered_checks()

    if not settings.ZOO_AUDITING_CHECKS:
        return

    site.addsitedir(str(settings.ZOO_AUDITING_ROOT))

    for package_name in settings.ZOO_AUDITING_CHECKS:
        package_kinds = _discover_kinds(package_name)
        KINDS.update(package_kinds)

        package_patches = _discover_patches(package_name, package_kinds)
        PATCHES.update(package_patches)


def _get_package_members(package, filter_by_re=None):
    for _, module_full_name, ispkg in pkgutil.walk_packages(
        path=package.__path__,
        prefix=package.__name__ + ".",
        onerror=log_error,
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
