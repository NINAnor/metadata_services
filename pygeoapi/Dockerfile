FROM busybox:latest AS build
ENV WATCHEXEC_VERSION=2.3.2
ENV WATCHEXEC_PLATFORM=x86_64-unknown-linux-musl
ADD https://github.com/watchexec/watchexec/releases/download/v${WATCHEXEC_VERSION}/watchexec-${WATCHEXEC_VERSION}-${WATCHEXEC_PLATFORM}.tar.xz /
RUN tar -xf watchexec-${WATCHEXEC_VERSION}-${WATCHEXEC_PLATFORM}.tar.xz --strip-components=1 watchexec-${WATCHEXEC_VERSION}-${WATCHEXEC_PLATFORM}/watchexec


FROM ghcr.io/osgeo/gdal:ubuntu-full-3.11.2 AS base
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install --no-install-recommends -yq \
    gettext curl build-essential python3-dev

WORKDIR /pygeoapi

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=build /watchexec /usr/local/bin/watchexec
COPY pyproject.toml uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-groups

COPY base.yml setup-conf.py .
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
