import json

openapi_spec = {
    "openapi": "3.0.0",
    "info": {"version": "1.0.0", "title": "Petstore"},
    "paths": {
        "/pets": {
            "get": {
                "summary": "List all pets",
                "operationId": "listPets",
                "responses": {"200": {"description": "ok"}},
            },
            "post": {
                "summary": "Create a pet",
                "operationId": "createPets",
                "responses": {"201": {"description": "ok"}},
            },
        },
        "/pets/{petId}": {
            "get": {
                "summary": "Info for a specific pet",
                "operationId": "showPetById",
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "description": "The id of the pet to retrieve",
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {"200": {"description": "ok"}},
            }
        },
    },
}

repo_files = {
    "readme.md": "Hello world!",
    "requirements.txt": "django==2.3.4",
    "package.json": '{"dependencies": {"webpack": "~0.0.0-rc14"}}',
    "openapi.json": json.dumps(openapi_spec),
}


def check_found(context):
    yield context.Result("check:found", True, {"answer": 42})


def check_passing(context):
    yield context.Result("check:passing", False)


CHECKS = [check_found, check_passing]
