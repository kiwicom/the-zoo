import os
from pathlib import Path

import raven


def _get_app_version():
    """Return current commit SHA of the app."""
    file_path = Path(__file__)
    for directory in file_path.parents:
        if (directory / ".git").exists():
            return raven.fetch_git_sha(str(directory))

    # if there was no git repo in the parent directories
    return os.getenv("PACKAGE_VERSION")


# borrow this file and add some utils here for graphql
