FROM node:12-alpine as fe-builder

ENV NODE_OPTIONS="--max-old-space-size=2048"

WORKDIR /app/webpack
COPY webpack ./
RUN yarn install --frozen-lockfile && \
    yarn cache clean

COPY zoo/ source/
RUN yarn production

FROM python:3.8-slim

ENV DJANGO_SETTINGS_MODULE=zoo.base.settings
ENV POETRY_VERSION=1.1.4

RUN addgroup --system macaque && \
    adduser --no-create-home --disabled-password --system --ingroup macaque macaque

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt update && \
    apt install -y --no-install-recommends build-essential ca-certificates libpq-dev python3-venv && \
    update-ca-certificates && \
    pip install --no-cache-dir poetry==$POETRY_VERSION && \
    poetry config virtualenvs.create false && \
    poetry install -v && \
    rm -r ~/.cache/pypoetry && \
    apt remove -y build-essential && \
    apt autoremove -y && \
    apt clean autoclean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=fe-builder /app/zoo ./zoo
COPY . ./

RUN poetry install -v && \
    poetry run python manage.py check && \
    mkdir -p /app/zoo/public/static && \
    poetry run python manage.py collectstatic --noinput && \
    chown -R macaque:macaque /app

ARG package_version
ENV PACKAGE_VERSION=$package_version

USER macaque

CMD [ "gunicorn", "zoo", "--config", ".misc/gunicorn_config.py" ]
EXPOSE 8080
LABEL name=zoo
