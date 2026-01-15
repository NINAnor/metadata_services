FROM geopython/pycsw:3.0.0-beta2

USER root

RUN mkdir data
ENV PYCSW_CONFIG=/home/pycsw/data/config.yml

COPY config.yml data/
RUN cd data && /venv/bin/pycsw-admin.py setup-repository --config $PYCSW_CONFIG

ENTRYPOINT [ "/venv/bin/python3", "/usr/local/bin/entrypoint.py" ]
