import importlib
import os
import time
from pathlib import Path, PosixPath
from typing import Tuple
from unittest import TestCase

import pytest

from zoo.auditing import check_discovery as uut

test_folder_dir = os.path.dirname(os.path.realpath(__file__))


def test_check_discovery__correct_modules(settings):
    check_modules = ("correct_first_module", "correct_second_module")

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    uut.discover_checks()
    from zoo.auditing.check_discovery import CHECKS, KINDS, PATCHES

    assert len(CHECKS) == 11

    assert {function.__name__ for function in CHECKS} == {
        "check_another_dummy_function",
        "check_dummy_function",
        "check_dummy_function_again",
    }

    for function in CHECKS:
        assert function() == (function.__name__ == "check_dummy_function")

    assert len(KINDS) == 3
    assert set(KINDS.keys()) == {
        "something:check_dummy_function",
        "something:check_another_dummy_function",
        "something:check_dummy_function_again",
    }
    assert len(PATCHES) == 2
    assert set(PATCHES.keys()) == {
        "something:check_dummy_function",
        "something:check_dummy_function_again",
    }
    assert KINDS["something:check_dummy_function"].apply_patch() is True
    assert (
        KINDS["something:check_dummy_function"].apply_patch
        == KINDS["something:check_dummy_function_again"].apply_patch
    )


def test_check_discovery__members_not_functions(settings):
    check_modules = ("members_not_functions",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    uut.discover_checks()
    from zoo.auditing.check_discovery import CHECKS, KINDS

    assert len(CHECKS) == 4

    assert {function.__name__ for function in CHECKS} == {
        "check_another_dummy_function",
        "check_dummy_function",
    }

    for function in CHECKS:
        assert function() == (function.__name__ == "check_dummy_function")

    assert len(KINDS) == 2
    assert set(KINDS.keys()) == {
        "something:check_dummy_function",
        "something:check_another_dummy_function",
    }


def test_check_discovery__incorrect_module(settings):
    check_modules = ("incorrect_module",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    uut.discover_checks()
    from zoo.auditing.check_discovery import CHECKS

    assert len(CHECKS) == 0


def test_check_discovery__missing_metadata(settings):
    check_modules = ("missing_metadata",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    with pytest.raises(FileNotFoundError):
        uut.discover_checks()


def test_check_discovery__incorrect_metadata(settings):
    check_modules = ("incorrect_metadata",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    with pytest.raises(uut.IncorrectCheckMetadataError):
        uut.discover_checks()


def test_check_discovery__only_folders_module(settings):
    check_modules = ("only_folders",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    uut.discover_checks()
    from zoo.auditing.check_discovery import CHECKS

    assert len(CHECKS) == 4

    assert {function.__name__ for function in CHECKS} == {
        "check_another_dummy_function",
        "check_dummy_function",
    }

    for function in CHECKS:
        assert function() == (function.__name__ == "check_dummy_function")


def test_check_discovery__non_existing_module(settings):
    check_modules = ("non_existing_module",)

    settings.ZOO_AUDITING_ROOT = Path(f"{test_folder_dir}/tasks")
    settings.ZOO_AUDITING_CHECKS = check_modules

    with pytest.raises(ModuleNotFoundError):
        uut.discover_checks()


dummy_kind = {
    "namespace": "planets",
    "category": "From whole Universe",
    "id": "earth",
    "title": "Earth",
    "description": "Our home planet",
}


def test_kind_severity__default():
    kind = uut.Kind(**dummy_kind)
    assert kind.severity == uut.Severity.UNDEFINED


@pytest.mark.parametrize("severity", uut.Severity)
def test_kind_severity__valid(severity):
    kind = uut.Kind(severity=severity.value, **dummy_kind)
    assert kind.severity == severity


def test_kind_severity__invalid():
    with pytest.raises(ValueError):
        uut.Kind(severity="wrong", **dummy_kind)


def test_kind_effort__default():
    kind = uut.Kind(**dummy_kind)
    assert kind.effort == uut.Effort.UNDEFINED


@pytest.mark.parametrize("effort", uut.Effort)
def test_kind_effort__valid(effort):
    kind = uut.Kind(effort=effort.value, **dummy_kind)
    assert kind.effort == effort


def test_kind_effort__invalid():
    with pytest.raises(ValueError):
        uut.Kind(effort="wrong", **dummy_kind)


@pytest.mark.parametrize(
    ("description", "details", "expected"),
    [
        ("Great {details}", None, "Great "),
        ("Space {details}", {}, "Space "),
        ("Mission {details}", {"details": "Apollo 11"}, "Mission Apollo 11"),
        (
            "Heroes: {astronauts}",
            {"astronauts": ["Armstrong", "Aldrin", "Collins"]},
            "Heroes: ['Armstrong', 'Aldrin', 'Collins']",
        ),
        ("Target: {missed}", {"target": "Sun"}, "Target: "),
    ],
)
def test_kind__format_description(description, details, expected, kind_factory):
    kind = kind_factory(description=description)
    assert kind.format_description(details) == expected
