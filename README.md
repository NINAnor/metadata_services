# Metadata services

This repository provides entrypoint scripts to generate configurations for `PyCSW` and `PyGeoAPI` in a composite and modular way.
Such configurations use file partitioning on object storage solutions to read partial configurations from multiple sources.

## Workflow example

### PyCSW
PyCSW entrypoint uses duckdb to populate a SQLite database with metadata.
Different services can then write different parquet files to expose such metadata, and DuckDB uses partitioned read to aggregate them and insert into the SQLite DB.

A metadata row should follow the [Metadata model reference](https://docs.pycsw.org/en/latest/metadata-model-reference.html#metadata-model-reference) of `pycsw`.
The `XML` property can be generated with [PyGeoMeta](https://github.com/geopython/pygeometa).

### PyGeoAPI
PyGeoAPI entrypoint reads a series of JSON files containing arrays of pygeoapi resources (https://docs.pygeoapi.io/en/latest/data-publishing/ogcapi-features.html).
All the resources are joined together with the base configuration.

- Reference for creating [resources](https://docs.pygeoapi.io/en/latest/configuration.html#resources)
- Reference for creating OGR providers of [vector resources](https://docs.pygeoapi.io/en/latest/data-publishing/ogcapi-features.html#ogr)

## Setup
Setup the variables accordingly.

```bash
docker compose up --build
```

## Rationale
`pygeoapi` and `pycsw` are very good software, but hard to integrate in other python softwares.
They are excellent when used statically (`pygeoapi` in particular is not very dynamic at runtime).
So the idea is to decouple the data sharing from the data storage, and use modern tools like DuckDB and Object Buckets as source of truth for the services.
Data should be provided in a static way (using Cloud Native Formats), and should be updated through some recurrent task.
Metadata and Configuration should also be treated as data, but stored in a different file set in the Object Storage.

The current implementation just add a thin wrapper over the original services, tipically a python or a bash script executed as entrypoint.
Such scripts will fetch the metadata and the configurations and adjust them in the way that the service requires:
- a SQLite DB is created for PyCSW, injected with the content of the parquet files stored in the Object Storage
- a YML file is created for PyGeoAPI, injected with the configurations read by JSON files stored in the Object Storage

### Pros of this approach
- Easy to update the original service
- Services are idempotent, with the same set of data/coonfiguration they produce the same result.
- Complexity is moved to a specialized task, that can depend on the source
- More control over what is published

### Cons of this approach
- Services must be restarted to get updates
- More infrastructure burden
- You need to have good control of your buckets :D
- Slower startup
