import json
import os

from django.core import serializers


def _get_app_version():
    return os.getenv("PACKAGE_VERSION")


def model_instance_to_json_object(model_instance):
    serialized_string = serializers.serialize(
        "json",
        [
            model_instance,
        ],
    )
    json_object = json.loads(serialized_string)
    return json_object[0]


# borrow this file and add some utils here for graphql
