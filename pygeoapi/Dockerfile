FROM ghcr.io/osgeo/gdal:ubuntu-full-3.10.1 AS base
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -yq \
    gettext curl build-essential python3-dev

WORKDIR /pygeoapi

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

COPY base.yml setup-conf.py .
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
