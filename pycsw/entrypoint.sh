#!/bin/bash

set -e
echo 'pulling data'
cp base.db data/records.db
duckdb ":memory:" "$(envsubst <query.sql)"
python3 /usr/local/bin/entrypoint.py
