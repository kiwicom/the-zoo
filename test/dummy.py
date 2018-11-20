repo_files = {
    "readme.md": "Hello world!",
    "requirements.txt": "django==2.3.4",
    "package.json": '{"dependencies": {"webpack": "~0.0.0-rc14"}}',
}


def check_found(context):
    yield context.Result("check:found", True, {"answer": 42})


def check_passing(context):
    yield context.Result("check:passing", False)


CHECKS = [check_found, check_passing]
