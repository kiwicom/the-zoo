from pathlib import Path

import yaml

from . import CiTemplate, DockerImage


def parse_gitlab_ci_template(parsed_yaml):
    """Parse gitlab-ci.yml file for names of templates."""
    for name in parsed_yaml.get("include", {}):
        yield CiTemplate(Path(name).stem)


def get_image(image_def):
    """Get names of docker images from yaml dict."""
    if image_def is None:
        return None

    if ":" in image_def:
        name, version = image_def.split(":")
    else:
        name = image_def
        version = "latest"

    if "$CI_REGISTRY_IMAGE" not in name:
        return DockerImage(name, version=version)


def parse_docker_images(parsed_yaml):
    """Parse gitlab-ci.yml file for names of docker images."""
    images = [get_image(parsed_yaml.get("image"))]
    images.extend(
        [
            get_image(job_def.get("image"))
            for job_def in parsed_yaml.values()
            if isinstance(job_def, dict)
        ]
    )

    yield from {image for image in images if image is not None}


def analyze(repository, path):
    """Parse gitlab-ci.yml to get the templates and the images."""
    gitlab_ci_file = path / ".gitlab-ci.yml"

    if not gitlab_ci_file.is_file():
        return

    parsed_yaml = yaml.safe_load(gitlab_ci_file.read_text())

    yield from parse_gitlab_ci_template(parsed_yaml)
    yield from parse_docker_images(parsed_yaml)
