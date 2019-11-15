import structlog

from ...repos.exceptions import RepositoryNotFoundError
from ...repos.utils import get_scm_module
from . import Language

log = structlog.get_logger()


def analyze(repository, _):
    """Search languages used in repo using git APIs."""
    scm_module = get_scm_module(repository.provider)
    try:
        langs = scm_module.get_languages(repository.remote_id)
    except RepositoryNotFoundError:
        log.exception("analytics.git_api.analyze.error")
        return
    for lang_name, usage in langs.items():
        if float(usage) > 5:
            yield Language(lang_name)
