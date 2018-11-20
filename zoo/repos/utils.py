import importlib
from pathlib import Path
import tarfile
import tempfile

from .exceptions import MissingFilesError, RepositoryNotFoundError


def get_scm_module(provider):
    """Return correct zoo.repos modul for Git API according to provider value.

    e.g.: repository.provider = 'gitlab' => return zoo.repos.gitlab
    """
    current_module = ".".join(__name__.split(".")[:-1])
    scm_module = importlib.import_module(f".{provider}", current_module)
    return scm_module


def download_repository(repository, repo_dir, sha=None):
    scm_module = get_scm_module(repository.provider)

    try:
        project = scm_module.get_project(repository.remote_id)
    except RepositoryNotFoundError as e:
        raise RepositoryNotFoundError(
            f"{repository} is private or doesn't exist."
        ) from e

    with tempfile.SpooledTemporaryFile(max_size=(10 * 1024 * 1024)) as archive:
        try:
            archive = scm_module.download_archive(project, archive, sha)
        except MissingFilesError as e:
            raise MissingFilesError(f"{repository} doesn't have any files.") from e

        archive.seek(0)
        with tarfile.open(fileobj=archive) as tar:
            inner_folder = tar.next().name
            tar.extractall(repo_dir)

    return Path(repo_dir) / inner_folder
