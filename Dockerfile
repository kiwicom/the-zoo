FROM python:3.7-alpine

ENV ZOO_RDS_PRODUCTION_CERT_PATH=/etc/ssl/certs/rds-combined-ca-bundle.pem \
    DJANGO_SETTINGS_MODULE=zoo.base.settings
RUN addgroup -S macaque && adduser -H -D -S macaque macaque

WORKDIR /app
COPY *requirements.txt ./
RUN apk add --no-cache --virtual=.build-deps curl build-base postgresql-dev && \
    apk add --no-cache --virtual=.run-deps libpq && \
    apk add --no-cache --virtual=.webpack-deps nodejs nodejs-npm && \
    # npm needs unsafe-perm because of https://github.com/nodejs/docker-node/issues/813
    npm config set unsafe-perm true && \
    npm install --global yarn && \
    curl -o $ZOO_RDS_PRODUCTION_CERT_PATH https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem && \
    pip install --no-cache-dir -r requirements.txt -r test-requirements.txt && \
    apk del .build-deps

WORKDIR /app/webpack
COPY webpack/ ./
RUN yarn install --frozen-lockfile && \
    yarn cache clean

COPY zoo/ source/
RUN yarn production && \
    rm -r node_modules source && \
    apk del .webpack-deps

WORKDIR /app
COPY . ./

ARG package_version
ENV PACKAGE_VERSION=$package_version
RUN pip install -e . && \
    python manage.py collectstatic --noinput && \
    chown -R macaque:macaque /app

USER macaque

CMD [ "gunicorn", "zoo", "--config", ".misc/gunicorn_config.py" ]
EXPOSE 8080
LABEL name=zoo
