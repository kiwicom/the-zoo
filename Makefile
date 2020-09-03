# makes `make test` target our test section, not the directory test/
.PHONY: test

curr_dir = $(shell pwd)

run:
	docker-compose up app webpack worker

run-detached:
	docker-compose up -d app webpack worker

run-scheduler:
	docker-compose up -d scheduler

stop:
	docker-compose stop

destroy:
	docker-compose down -v

test:
	TOX_TESTENV_PASSENV=TEST_DATABASE_URL tox

pytest:
	.tox/tests/bin/py.test

fake:
	docker-compose run app python manage.py fake

migrate:
	docker-compose run app python manage.py migrate

migrations:
	docker-compose run app python manage.py makemigrations

superuser:
	docker-compose run app python manage.py createsuperuser

shell:
	docker-compose run app python manage.py shell_plus

build-docs:
	(cd docs && make html)

open-docs:
	open docs/_build/html/index.html
