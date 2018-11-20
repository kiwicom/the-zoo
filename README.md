# zoo

| What       | Where                                                              |
| ---------- | ------------------------------------------------------------------ |
| Discussion | [#the-zoo on Slack](https://skypicker.slack.com/messages/the-zoo/) |
| Maintainer | [Alex Viscreanu](https://gitlab.skypicker.com/aexvir/)             |

## Development

- Run in debug mode: `$ make run`
- Stop: `$ make stop`
- Stop and/or delete data: `$ make destroy`
- Django shell: `$ make shell`
- Containers logs: `$ docker-compose logs`

Access web locally:

- Web is running on port `20966`
- Login at <http://localhost:20966/admin> with your superuser account
- Access zoo at <http://localhost:20966/>

### Initial setup

- Create a database: `$ make migrate`
- Create a superuser: `$ make superuser`

### Database changes

- Generate database migrations: `$ make makemigrations`
- Update the database when needed: `$ make migrate`

### Notes

Check `Makefile` for shell commands if you want to run them with modified
parameters.

## Testing

Run all tests: `$ make test`

Tests are run by `tox`. In order to run only unit tests or a specific test file 
you need to use the `pytest` binary from the `.tox/tests/bin/` folder. This
folder will be created after running tests for the first time.

### Testing requirements

PostgreSQL is needed for running the integration tests, you can install it by
running `brew install postgres`

Note that this includes running `dockerfile_lint` and `remark`, which you can
get with `npm install -g dockerfile_lint remark-cli`.

Also note that tox doesn't know when you change the `requirements.txt`
and won't automatically install new dependencies for test runs.
Run `pip install tox-battery` to install a plugin which fixes this silliness.

If you want to pass some env vars to environment, you can list them in env var
`TOX_TESTENV_PASSENV`. For example if you want to use custom database for tests,
you can run: `TEST_DATABASE_URL=postgres://... TOX_TESTENV_PASSENV=TEST_DATABASE_URL tox`

## Documentation

### Architecture Decision Records

We document architecture decisions like it's described in 
[this article](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

Records are in dir `adr`. We are using [ADR Tools](https://github.com/npryce/adr-tools)
for working with them.

### Documentation for users

We use [Sphinx](http://www.sphinx-doc.org/) for generating documentation. Docs
are in dir `docs`.

Setup virtual enviroment and install there `docs-requirements.txt`. Then you can
use shortcuts:

- Build docs: `$ make build-docs`
- Open docs: `$ make read-docs` 
