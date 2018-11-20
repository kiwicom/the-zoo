from dockerfile_parse import DockerfileParser

from . import Language, OS
from ..models import DependencyType
from .utils import parse_version

KNOWN_DEPS = {
    DependencyType.LANG: {"python", "node"},
    DependencyType.OS: {"alpine", "debian"},
}
KNOWN_DEBIAN_IMAGES = {"python", "node"}


def analyze(repository, path):
    """Parse dockerfile for image information about platform."""
    dockerfile = path / "Dockerfile"
    if not dockerfile.is_file():
        return
    dfp = DockerfileParser(path=dockerfile.name)
    for command in dfp.structure:
        if command["instruction"] != "FROM":
            continue
        yield from parse_base_image_name(command["value"], repository=repository)


def parse_base_image_name(base_image: str, repository):
    lang_fragment, _, os_fragment = base_image.partition("-")
    for lang_name in KNOWN_DEPS[DependencyType.LANG]:
        if lang_name not in lang_fragment:
            continue
        lang_version = parse_version(lang_fragment.replace(lang_name, "").strip(": "))
        yield Language(lang_name, lang_version, for_production=True)

        if "alpine" in os_fragment:
            os_version = parse_version(os_fragment.replace("alpine", "").strip(": "))
            yield OS("alpine", os_version, for_production=True)
        elif lang_name in KNOWN_DEBIAN_IMAGES:
            yield OS("debian", for_production=True)
