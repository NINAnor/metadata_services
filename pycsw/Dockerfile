FROM geopython/pycsw:3.0.0-beta1

USER root
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends curl gettext

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir data

ENV PYCSW_CONFIG=/home/pycsw/data/config.yml

COPY config.yml records.db data/
COPY pull.py /usr/local/bin/pull_data

ENTRYPOINT [ "python3", "/usr/local/bin/entrypoint.py" ]
