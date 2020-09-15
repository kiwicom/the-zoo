import os


def _get_app_version():
    return os.getenv("PACKAGE_VERSION")


# borrow this file and add some utils here for graphql
