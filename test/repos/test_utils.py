import tempfile
from pathlib import Path

import fakeredis
import pytest

import zoo.repos.utils as uut
from zoo.repos.exceptions import MissingFilesError, RepositoryNotFoundError
from zoo.repos.models import Provider
from zoo.repos.utils import get_scm_module

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_download_repository__project_does_not_exist(fake_dir, repository, mocker):
    scm_module = get_scm_module(repository.provider)
    m_get_project = mocker.patch.object(
        scm_module, "get_project", side_effect=RepositoryNotFoundError
    )

    with pytest.raises(uut.RepositoryNotFoundError):
        uut.download_repository(repository, fake_dir)

    m_get_project.assert_called_once_with(repository.remote_id)


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_download_repository__missing_files(fake_dir, repository, mocker):
    scm_module = get_scm_module(repository.provider)
    m_get_project = mocker.patch.object(
        scm_module, "get_project", return_value=mocker.sentinel.project
    )
    m_download_archive = mocker.patch.object(
        scm_module, "download_archive", side_effect=MissingFilesError
    )

    with pytest.raises(uut.MissingFilesError):
        uut.download_repository(repository, fake_dir)

    m_get_project.assert_called_once_with(repository.remote_id)
    m_download_archive.assert_called_once_with(
        mocker.sentinel.project, mocker.ANY, None
    )


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_download_repository(fake_dir, repo_archive, repository, mocker):
    scm_module = get_scm_module(repository.provider)
    m_get_project = mocker.patch.object(
        scm_module, "get_project", return_value=mocker.sentinel.project
    )
    m_download_archive = mocker.patch.object(
        scm_module, "download_archive", return_value=repo_archive
    )

    repo_path = uut.download_repository(repository, fake_dir)

    assert {f.name for f in repo_path.iterdir()} == {
        "readme.md",
        "requirements.txt",
        "package.json",
        "openapi.json",
    }
    assert (repo_path / "readme.md").read_text() == "Hello world!"

    m_get_project.assert_called_once_with(repository.remote_id)
    m_download_archive.assert_called_once_with(
        mocker.sentinel.project, mocker.ANY, None
    )


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_download_repository__custom_sha(fake_dir, repo_archive, repository, mocker):
    scm_module = get_scm_module(repository.provider)
    m_get_project = mocker.patch.object(
        scm_module, "get_project", return_value=mocker.sentinel.project
    )
    m_download_archive = mocker.patch.object(
        scm_module, "download_archive", return_value=repo_archive
    )

    sha = "idspispopd"
    repo_path = uut.download_repository(repository, fake_dir, sha)
    assert {f.name for f in repo_path.iterdir()} == {
        "readme.md",
        "requirements.txt",
        "package.json",
        "openapi.json",
    }
    assert (repo_path / "readme.md").read_text() == "Hello world!"

    m_get_project.assert_called_once_with(repository.remote_id)
    m_download_archive.assert_called_once_with(mocker.sentinel.project, mocker.ANY, sha)


@pytest.mark.parametrize("repository__provider", [item.value for item in Provider])
def test_openapi_definition(fake_path, repo_archive, repository, mocker):
    scm_module = get_scm_module(repository.provider)
    m_get_project = mocker.patch.object(
        scm_module, "get_project", return_value=mocker.sentinel.project
    )
    m_download_archive = mocker.patch.object(
        scm_module, "download_archive", return_value=repo_archive
    )

    fake_path.mkdir(parents=True, exist_ok=True)
    mocker.patch("tempfile.mkdtemp", return_value=str(fake_path))
    mocker.patch("zoo.repos.utils.OPENAPI_SCAN_EXCLUDE", [])

    def redis(**kwargs):
        return fakeredis.FakeStrictRedis(**kwargs)

    mocker.patch("zoo.base.redis.get_connection", redis)

    specs = uut.openapi_definition(repository)

    m_get_project.assert_called_once_with(repository.remote_id)
    m_download_archive.assert_called_once_with(
        mocker.sentinel.project, mocker.ANY, None
    )

    assert len(specs) == 1  # spec is readable
    assert specs[0]["info"]["title"] == "Petstore"
    assert specs[0]["info"]["version"] == "1.0.0"
    assert not fake_path.exists()  # cleaned up
