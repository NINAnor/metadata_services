FROM geopython/pycsw:3.0.0-beta2

USER root
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends curl gettext

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN mkdir data

ENV PYCSW_CONFIG=/home/pycsw/data/config.yml

COPY config.yml records.db data/
COPY pull.py pyproject.toml uv.lock .
RUN uv sync --frozen

ENTRYPOINT [ "/venv/bin/python3", "/usr/local/bin/entrypoint.py" ]
