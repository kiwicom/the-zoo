# makes `make test` target our test section, not the directory test/
.PHONY: test


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
	tox

pytest:
	.tox/tests/bin/py.test

migrate:
	docker-compose run app python manage.py migrate

makemigrations:
	docker-compose run app python manage.py makemigrations

superuser:
	docker-compose run app python manage.py createsuperuser

shell:
	docker-compose run app python manage.py shell_plus

build-docs:
	(cd docs && make html)

open-docs:
	open docs/_build/html/index.html
