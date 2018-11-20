# makes `make test` target our test section, not the directory test/
.PHONY: test


run:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up app webpack worker

run-detached:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d app webpack worker

run-scheduler:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d scheduler

stop:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml stop

destroy:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v

test:
	tox

pytest:
	.tox/tests/bin/py.test

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run app python manage.py migrate

makemigrations:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run app python manage.py makemigrations

superuser:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run app python manage.py createsuperuser

shell:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run app python manage.py shell_plus

build-docs:
	(cd docs && make html)

open-docs:
	open docs/_build/html/index.html
