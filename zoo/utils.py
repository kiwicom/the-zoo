import os
from pathlib import Path

import raven


def _get_app_version():
    """Return current commit SHA of the app."""
    basedir = Path(__file__).parent
    if (basedir / ".git").exists():
        return raven.fetch_git_sha(str(basedir))

    # if there was no git repo in the parent directories
    return os.getenv("PACKAGE_VERSION")


# borrow this file and add some utils here for graphql
