import re
from typing import Optional

import structlog

log = structlog.get_logger()


def parse_version(raw_version: str) -> str:
    """Resolve semantic versioning used in javascript packages."""
    try:
        validate_version(raw_version)
    except ValueError:
        log.exception("analytics.utils.parse_version.error", raw_version=raw_version)
        return None

    if "=" in raw_version:
        return raw_version.split("=")[1]
    if raw_version.startswith("^"):
        return resolve_caret_version(raw_version)
    if raw_version.startswith("~"):
        return resolve_tilde_version(raw_version)
    return resolve_unknown_format(raw_version)


def validate_version(version: str) -> bool:  # Ignore RadonBear
    if not version:
        raise ValueError("Version given is an empty string?!?!¿!?")
    if version.count(".") > 2:
        raise ValueError(f"Version {version} has too many dots")
    if not any(True for char in version if char.isdigit()):
        raise ValueError(f"Version {version} has no digits in it")
    if " " in version or "||" in version or "#" in version:
        raise ValueError(f"Version {version} has unsupported version specifiers")
    if ("<" in version or ">" in version) and "=" not in version:
        raise ValueError(f"Version {version} has unsupported version specifiers")


def resolve_caret_version(version: str) -> str:
    temp_version = ""
    for version_digit in version[1:].split("."):
        temp_version += version_digit
        if version_digit.isdigit() and int(version_digit) != 0:
            break
        temp_version += "."
    return temp_version


def resolve_tilde_version(version: str) -> str:
    version = version[1:].split(".")
    if any(True for version_digit in version[:~0] if int(version_digit) != 0):
        del version[~0]
    return ".".join(version)


def resolve_unknown_format(version: str) -> str:
    temp_version = []
    for version_digit in version.split("."):
        if version_digit.isdigit():
            temp_version.append(version_digit)
        else:
            break
    return ".".join(temp_version)


class DockerImageId:
    """Represents parsed docker image id."""

    # pylint: disable=too-many-instance-attributes # Ignore PyCommentedCodeBear

    def __init__(self, image: str):  # Ignore RadonBear
        self.__full_image_id = " ".join(image.split())

        self.__registry = None
        self.__registry_host_name = None
        self.__registry_port = None
        self.__full_image_name = None
        self.__full_image_name_no_tag = None
        self.__username = None
        self.__full_repository_name = None
        self.__repository_name = None
        self.__namespaces = None
        self.__tag = None
        self.__version = None
        self.__full_os = None
        self.__os = None
        self.__os_version = None
        self.__alias = None

    @property
    def full_image_id(self) -> str:
        """Full provided image identifier."""
        return self.__full_image_id

    @property
    def registry(self) -> str:
        """Docker registry.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        Docker registry is recognised as:
            a) "localhost" present before first "/" of the full docker id.
            b) "." present before first "/" of the full docker id.
        """
        if "/" in self.full_image_id:
            registry_part, _, _ = self.full_image_id.partition("/")
            if "localhost" in registry_part or "." in registry_part:
                # This really is a registry string.
                self.__registry, _, _ = self.full_image_id.partition("/")

        return self.__registry

    @property
    def registry_host_name(self) -> str:
        """Docker registry host name.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        self.__registry_host_name = self.registry

        if self.registry and ":" in self.registry:
            self.__registry_host_name, _, _ = self.registry.partition(":")

        return self.__registry_host_name

    @property
    def registry_port(self) -> str:
        """Docker registry port.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                        ‾‾‾‾
        """
        if self.registry and ":" in self.registry:
            _, _, self.__registry_port = self.registry.partition(":")

        return self.__registry_port

    @property
    def full_image_name(self) -> str:
        """Whole name of the image without the registry.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        self.__full_image_name = self.full_image_id

        if self.registry:
            _, _, self.__full_image_name = self.full_image_id.partition("/")

        return self.__full_image_name

    @property
    def tag(self) -> str:
        """Tag.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                               ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        if ":" in self.full_image_name:
            _, _, self.__tag = self.full_image_name.partition(":")

            if " as " in self.__tag:
                self.__tag, _, _ = self.__tag.partition(" as ")

        return self.__tag

    @property
    def full_image_name_no_tag(self) -> str:
        """Full image name without the tag and alias.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                             ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        self.__full_image_name_no_tag, _, _ = self.full_image_name.partition(":")
        self.__full_image_name_no_tag, _, _ = self.__full_image_name_no_tag.partition(
            " as "
        )

        return self.__full_image_name_no_tag

    @property
    def username(self) -> str:
        """Username (first part of the image path by convention).

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                             ‾‾‾‾‾‾‾‾‾‾‾‾
        """
        if "/" in self.full_image_name_no_tag:
            self.__username, _, _ = self.full_image_name_no_tag.partition("/")

        return self.__username

    @property
    def full_repository_name(self) -> str:
        """Full repository name without "username".

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                          ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        self.__full_repository_name = self.full_image_name_no_tag

        if "/" in self.__full_repository_name:
            _, _, self.__full_repository_name = self.__full_repository_name.partition(
                "/"
            )

        return self.__full_repository_name

    @property
    def repository_name(self) -> str:
        """First part of the full repository name path (repository name by convention).

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                          ‾‾‾‾‾‾‾‾
        """
        self.__repository_name = self.full_repository_name

        if "/" in self.__repository_name:
            # Take the first part as repo name if there still are more slashes present.
            self.__repository_name, _, _ = self.__repository_name.partition("/")

        return self.__repository_name

    @property
    def namespaces(self) -> []:
        """"Namespaces" - all path parts after username and image name as a list.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
        """
        if "/" in self.full_repository_name:
            _, _, namespaces = self.full_repository_name.partition("/")
            self.__namespaces = namespaces.split("/")

        return self.__namespaces

    @property
    def alias(self) -> str:
        """Image identifier alias.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                                                  ‾‾‾‾‾‾‾‾‾‾
        """
        if " as " in self.full_image_id:
            _, _, self.__alias = self.full_image_id.partition(" as ")

        return self.__alias

    @property
    def version(self) -> str:
        """Version of the image.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                               ‾‾‾‾‾
        """
        self.__version = self.tag

        if self.__version and "-" in self.__version:
            self.__version, _, _ = self.tag.partition("-")

        return self.__version

    @property
    def full_os(self) -> str:
        """OS part - parsed from tag when "-" is present.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                                     ‾‾‾‾‾‾‾‾‾
        """
        if self.tag and "-" in self.tag:
            _, _, self.__full_os = self.tag.partition("-")

        return self.__full_os

    @property
    def os(self) -> str:
        """OS without version.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                                     ‾‾‾‾‾‾
        """
        self.__os = self.__full_os

        if self.full_os:
            os_version = self.__parse_semantic_version(self.__full_os)

            if os_version:
                self.__os = self.__full_os.replace(os_version, "")

        return self.__os

    @property
    def os_version(self) -> str:
        """OS version.

        my.registry.com:5005/special-name/my-image/namespace/another-namespace:0.1.1-alpine3.9 as base-image
                                                                                           ‾‾‾
        """
        self.__os_version = self.__parse_semantic_version(self.__full_os)

        return self.__os_version

    @staticmethod
    def __parse_semantic_version(string: Optional[str]) -> Optional[str]:
        """Parse semantic version from provided input."""
        if string:
            match = re.search(r"\d+[\d|\.]*\d", string)
            if match:
                return match.group()
        return None

    def __str__(self):
        return str(self.__dict__)
