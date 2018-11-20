import json

import structlog

from . import JSLibrary
from .utils import parse_version

log = structlog.get_logger()


def analyze(repository, path):
    """Parse package.json for javascript packages."""
    package_json_path = path / "package.json"
    if not package_json_path.is_file():
        return
    try:
        package_json = json.loads(package_json_path.read_text())
    except json.decoder.JSONDecodeError:
        log.exception("analytics.package_json.analyze.error")
        return
    for dependency_key, for_production in [
        ("peerDependencies", None),
        ("devDependencies", False),
        ("dependencies", True),
    ]:
        dependencies = package_json.get(dependency_key)
        if not dependencies:
            continue

        for lib_name, lib_version in dependencies.items():
            yield JSLibrary(lib_name, parse_version(lib_version), for_production)
