#!/bin/bash

set -e
echo 'pulling data'
uv run setup-conf.py


export PYGEOAPI_HOME=/pygeoapi
export PYGEOAPI_CONFIG="${PYGEOAPI_HOME}/local.config.yml"
export PYGEOAPI_OPENAPI="${PYGEOAPI_HOME}/local.openapi.yml"

SCRIPT_NAME=${SCRIPT_NAME:=/}
CONTAINER_NAME=${CONTAINER_NAME:=pygeoapi}
CONTAINER_HOST=${CONTAINER_HOST:=0.0.0.0}
CONTAINER_PORT=${CONTAINER_PORT:=80}
WSGI_APP=${WSGI_APP:=pygeoapi.flask_app:APP}
WSGI_WORKERS=${WSGI_WORKERS:=4}
WSGI_WORKER_TIMEOUT=${WSGI_WORKER_TIMEOUT:=6000}
WSGI_WORKER_CLASS=${WSGI_WORKER_CLASS:=gevent}

uv run pygeoapi openapi generate ${PYGEOAPI_CONFIG} --output-file ${PYGEOAPI_OPENAPI}

# SCRIPT_NAME should not have value '/'
[[ "${SCRIPT_NAME}" = '/' ]] && export SCRIPT_NAME="" && echo "make SCRIPT_NAME empty from /"

echo "Starting gunicorn name=${CONTAINER_NAME} on ${CONTAINER_HOST}:${CONTAINER_PORT} with ${WSGI_WORKERS} workers and SCRIPT_NAME=${SCRIPT_NAME}"
uv run gunicorn --workers ${WSGI_WORKERS} \
    --worker-class=${WSGI_WORKER_CLASS} \
    --timeout ${WSGI_WORKER_TIMEOUT} \
    --name=${CONTAINER_NAME} \
    --bind ${CONTAINER_HOST}:${CONTAINER_PORT} \
    ${@} \
    ${WSGI_APP}