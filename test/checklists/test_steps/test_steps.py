import os
from pathlib import Path

import pytest

from zoo.checklists import steps as uut

pytestmark = pytest.mark.django_db

test_folder_dir = os.path.dirname(os.path.realpath(__file__))


def test_steps__no_yaml_files(settings, fake_dir):
    checklists_root = Path(fake_dir)
    settings.ZOO_CHECKLISTS_ROOT = checklists_root

    uut.load_all_steps()

    steps = uut.load_all_steps()
    assert len(steps) == 0


def test_steps__with_yaml_files__invalid_file(settings):
    settings.ZOO_CHECKLISTS_ROOT = Path(f"{test_folder_dir}/steps/invalid_file/")

    with pytest.raises(uut.InvalidStepMetadata):
        steps = uut.load_all_steps()


def test_steps__with_yaml_files__valid_file__incorrect_header(settings):
    settings.ZOO_CHECKLISTS_ROOT = Path(f"{test_folder_dir}/steps/incorrect_header/")

    with pytest.raises(uut.IncorrectStepMetadata):
        steps = uut.load_all_steps()


def test_steps__with_yaml_files__valid_file__incorrect_content(settings):
    settings.ZOO_CHECKLISTS_ROOT = Path(f"{test_folder_dir}/steps/incorrect_content/")

    with pytest.raises(uut.IncorrectStepMetadata):
        steps = uut.load_all_steps()


def test_steps__with_yaml_files__valid_file__correct(settings):
    settings.ZOO_CHECKLISTS_ROOT = Path(f"{test_folder_dir}/steps/correct/")

    steps = uut.load_all_steps()
    assert len(steps) == 1
    assert "general" in steps
    assert "general:announce-service" in steps["general"]

    step = steps["general"]["general:announce-service"]

    assert step.tag == "general"
    assert step.category_name == "General services"
    assert step.id == "announce-service"
    assert step.title == "Announce your service in the channel"
    assert (
        step.description
        == "Sharing is caring, ya know. Let people know what you're about to put in production!\n"
    )
    assert step.help_url == "https://google.com"
