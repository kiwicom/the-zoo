FROM python:3.8-slim

ENV DJANGO_SETTINGS_MODULE=zoo.base.settings
RUN addgroup --system macaque && \
    adduser --no-create-home --disabled-password --system --ingroup macaque macaque

WORKDIR /app

COPY requirements/*.txt ./

RUN apt update && \
    apt install -y --no-install-recommends build-essential ca-certificates libpq-dev && \
    update-ca-certificates && \
    pip install --no-cache-dir -r base.txt -r test.txt && \
    apt remove -y build-essential && \
    apt autoremove -y && \
    apt clean autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm *.txt

COPY zoo ./zoo
COPY requirements ./requirements
COPY scripts ./scripts
COPY .misc ./.misc
COPY manage.py ./
COPY setup.py ./
COPY MANIFEST.in ./

RUN pip install --no-cache-dir -e . && \
    django-admin check && \
    mkdir -p /app/zoo/public/static && \
    django-admin collectstatic --noinput && \
    chown -R macaque:macaque /app && \
    rm -rf requirements

ARG package_version
ENV PACKAGE_VERSION=$package_version

USER macaque

CMD [ "gunicorn", "zoo", "--config", ".misc/gunicorn_config.py" ]
EXPOSE 8080
LABEL name=zoo
