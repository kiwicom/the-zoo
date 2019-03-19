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
        else:
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
