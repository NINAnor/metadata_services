#!/bin/bash

set -e
echo 'reset database'
yes | cp -rf base.db data/records.db
echo 'pulling data'
duckdb ":memory:" "$(envsubst <query.sql)" 2>&1 || true
echo 'loaded data'
python3 /usr/local/bin/entrypoint.py
