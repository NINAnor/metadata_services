FROM geopython/pycsw:3.0.0-beta1

USER root
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends curl gettext

ENV PATH="/root/.duckdb/cli/latest:$PATH"
RUN <<EOF
curl https://install.duckdb.org | sh
duckdb ":memory:" "install sqlite;install httpfs;"
mkdir data
EOF

ENV PYCSW_CONFIG=/home/pycsw/data/config.yml

COPY config.yml data/config.yml
COPY base.db query.sql .
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
