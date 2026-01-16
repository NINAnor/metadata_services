#!/bin/bash

set -e

export PYGEOAPI_HOME=${PYGEOAPI_HOME:="/pygeoapi/config"}
export PYGEOAPI_CONFIG="${PYGEOAPI_HOME}/local.config.yml"
export PYGEOAPI_OPENAPI="${PYGEOAPI_HOME}/local.openapi.yml"

CONTAINER_NAME=${CONTAINER_NAME:=pygeoapi}
CONTAINER_HOST=${CONTAINER_HOST:=0.0.0.0}
CONTAINER_PORT=${CONTAINER_PORT:=80}
WSGI_APP=${WSGI_APP:=pygeoapi.flask_app:APP}
WSGI_WORKERS=${WSGI_WORKERS:=4}
WSGI_WORKER_TIMEOUT=${WSGI_WORKER_TIMEOUT:=6000}
WSGI_WORKER_CLASS=${WSGI_WORKER_CLASS:=gevent}

uv run pygeoapi openapi generate ${PYGEOAPI_CONFIG} --output-file ${PYGEOAPI_OPENAPI}

echo "Starting gunicorn name=${CONTAINER_NAME} on ${CONTAINER_HOST}:${CONTAINER_PORT} with ${WSGI_WORKERS} workers"
watchexec -rw "$PYGEOAPI_CONFIG" --fs-events modify --stop-timeout 5s -- exec "uv run gunicorn --workers ${WSGI_WORKERS} \
    --worker-class=${WSGI_WORKER_CLASS} \
    --timeout ${WSGI_WORKER_TIMEOUT} \
    --name=${CONTAINER_NAME} \
    --bind ${CONTAINER_HOST}:${CONTAINER_PORT} \
    ${@} \
    ${WSGI_APP}"
