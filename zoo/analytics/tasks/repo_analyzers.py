from django.utils import timezone
import structlog

from . import docker, git_api, package_json, requirements_py
from ..models import Dependency, DependencyUsage

log = structlog.get_logger()

ANALYZERS = [docker, git_api, package_json, requirements_py]


def unpack_version(version: str) -> dict:
    version = version.split(".") if version else None
    if not version:
        return {}
    return {
        "major_version": version[0] if version and version[0].isdigit() else None,
        "minor_version": (
            version[1] if len(version) > 1 and version[1].isdigit() else None
        ),
        "patch_version": (
            version[2] if len(version) > 2 and version[2].isdigit() else None
        ),
    }


def run_all(repository, path):
    for module in ANALYZERS:
        analyzer = getattr(module, "analyze")
        log.info("repo.analyzer", repo=repository, check=module.__name__)
        for hit in analyzer(repository, path):
            dep, _ = Dependency.objects.update_or_create(
                name=hit.name, type=hit.type.value
            )
            dep.health_status = hit.health_status
            dep.save()
            dep.full_clean()

            dep_usage_defaults = unpack_version(hit.version)
            dep_usage_defaults["version"] = hit.version
            if hit.for_production is not None:
                dep_usage_defaults["for_production"] = hit.for_production

            if dep_usage_defaults:
                dep_usage_defaults["timestamp"] = timezone.now

            dep_usage, _ = DependencyUsage.objects.update_or_create(
                dependency=dep, repo=repository, defaults=dep_usage_defaults
            )
            dep_usage.full_clean()
