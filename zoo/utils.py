import json
import os
from pathlib import Path

import raven
from django.core import serializers


def _get_app_version():
    """Return current commit SHA of the app."""
    basedir = Path(__file__).parent
    if (basedir / ".git").exists():
        return raven.fetch_git_sha(str(basedir))

    # if there was no git repo in the parent directories
    return os.getenv("PACKAGE_VERSION")


def model_instance_to_json_object(model_instance):
        serialized_string = serializers.serialize('json', [model_instance, ])
        json_object = json.loads(serialized_string)
        return json_object[0]

# borrow this file and add some utils here for graphql
