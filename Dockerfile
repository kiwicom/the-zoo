FROM node:12-alpine as fe-builder

ENV NODE_OPTIONS="--max-old-space-size=2048"

WORKDIR /app/webpack
COPY webpack ./
RUN yarn install --frozen-lockfile && \
    yarn cache clean

COPY zoo/ source/
RUN yarn production

FROM python:3.7-alpine

ENV DJANGO_SETTINGS_MODULE=zoo.base.settings
RUN addgroup -S macaque && adduser -H -D -S macaque macaque

WORKDIR /app

COPY --from=fe-builder /app/zoo ./zoo
COPY requirements/*.txt ./

RUN apk add --no-cache --virtual=.build-deps build-base postgresql-dev icu-dev pkgconfig && \
    apk add --no-cache --virtual=.run-deps libpq icu-libs && \
    pip install --no-cache-dir -r base.txt -r test.txt && \
    apk del .build-deps

COPY . ./

RUN pip install -e . && \
    python manage.py check && \
    python manage.py collectstatic --noinput && \
    chown -R macaque:macaque /app

ARG package_version
ENV PACKAGE_VERSION=$package_version

USER macaque

CMD [ "gunicorn", "zoo", "--config", ".misc/gunicorn_config.py" ]
EXPOSE 8080
LABEL name=zoo
