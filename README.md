# Metadata services

This repository provides entrypoint scripts to generate configurations for `PyCSW` and `PyGeoAPI` in a composite and modular way.
Such configurations use file partitioning on object storage solutions to read partial configurations from multiple sources.

## Workflow example

### PyCSW
PyCSW entrypoint uses duckdb to populate a SQLite database with metadata read from a certain path (configurable).
Different services can then write different parquet files to expose such metadata.
An example can be found in https://github.com/NINAnor/dwca-parquet/blob/main/src/dwca_parquet/libs/csw.py

### PyGeoAPI
PyGeoAPI entrypoint reads a series of JSON files containing arrays of pygeoapi resources (https://docs.pygeoapi.io/en/latest/data-publishing/ogcapi-features).
All the resources are joined together with the base configuration.
An example of how resources can be generated can be found in https://github.com/NINAnor/dwca-parquet/blob/main/src/dwca_parquet/libs/geoapi.py

## Setup
```bash
docker compose up --build
```