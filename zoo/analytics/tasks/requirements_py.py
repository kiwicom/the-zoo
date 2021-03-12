import re

import arrow
import requirements
import structlog
from pkg_resources import RequirementParseError

from ...base.http import session
from . import PyLibrary

log = structlog.get_logger()


def analyze(repository, path):
    """Parse requirements files for python packages."""
    req_file_paths = path.glob("*requirements*.txt")
    for req_file_path in req_file_paths:
        if req_file_path.name == "requirements.txt":
            for_production = True
        elif req_file_path.name in {
            "test-requirements.txt",
            "dev-requirements.txt",
            "build-requirements.txt",
            "docs-requirements.txt",
        }:
            for_production = False
        else:
            for_production = None

        yield from _get_packages(
            req_file_path=req_file_path,
            repository=repository,
            path=path,
            for_production=for_production,
        )


def _get_packages(req_file_path, repository, path, for_production):
    try:
        reqs = list(requirements.parse(open(req_file_path, "r")))
        unhealthy_packages = get_unhealthy_packages(reqs)

        for requirement in reqs:
            lib_version = None

            if requirement.specs:
                version_specifier, lib_version = requirement.specs[0]
                if "=" not in version_specifier:
                    lib_version = None

            if requirement.name:
                health_status = requirement.name not in unhealthy_packages
                yield PyLibrary(
                    requirement.name, lib_version, for_production, health_status
                )

    except (RequirementParseError, ValueError):
        log.exception("analytics.requirements_py.analyze.error")
        return


def get_development_status_classifiers(classifiers: list) -> list:
    status_classifiers = []

    for classifier in classifiers:
        classifier_title = re.match(
            r"Development\sStatus\s\:\:\s(\d)\s\-\s\w+", classifier
        )

        if classifier_title:
            status_classifiers.append(classifier_title[1])

    return status_classifiers


def is_package_unhealthy(status: int, last_release_date: str) -> bool:
    now = arrow.utcnow()
    updated_ago = now - arrow.get(last_release_date)

    return any(
        [
            (status == 1),
            (status == 7),
            (status <= 3 and updated_ago.days > 30),
            (status == 4 and updated_ago.days > 60),
            (status >= 5 and updated_ago.days > 360),
        ]
    )


def get_pypi_metadata(package_name: str):
    r = session.get(f"https://pypi.org/pypi/{package_name}/json")
    return None if r.status_code == 404 else r.json()


def get_unhealthy_packages(reqs: list) -> list:
    unhealthy_packages = []

    for req in reqs:
        if req.name is None:
            continue

        package_metadata = get_pypi_metadata(req.name)
        if package_metadata is None:
            continue

        status_classifiers = get_development_status_classifiers(
            package_metadata["info"]["classifiers"]
        )

        if len(status_classifiers) != 1:
            unhealthy_packages.append(req.name)
            continue

        status = status_classifiers[0]
        current_version = package_metadata["info"]["version"]

        if is_package_unhealthy(
            int(status), package_metadata["releases"][current_version][0]["upload_time"]
        ):
            unhealthy_packages.append(req.name)

    return unhealthy_packages
