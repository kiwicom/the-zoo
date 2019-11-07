from pathlib import Path

from . import DockerImage, OS
from ..models import DependencyType
from .utils import DockerImageId

KNOWN_DEPS = {
    DependencyType.LANG: {"python", "node"},
    DependencyType.OS: {"alpine", "debian"},
}
KNOWN_DEBIAN_IMAGES = {"python", "node"}


def analyze(repository, path: Path):
    """Parse dockerfiles for image information."""
    for dockerfile in path.rglob("Dockerfile*"):
        with open(dockerfile.as_posix()) as f:
            for line in f:
                cmd, _, val = line.partition(" ")

                if "FROM" not in cmd.upper():
                    continue

                parsed_image_id = DockerImageId(val)

                yield DockerImage(
                    name=parsed_image_id.repository_name,
                    version=parsed_image_id.version,
                    for_production=True,
                )

                if parsed_image_id.os:
                    yield OS(
                        name=parsed_image_id.os,
                        version=parsed_image_id.os_version,
                        for_production=True,
                    )
