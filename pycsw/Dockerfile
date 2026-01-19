FROM geopython/pycsw:3.0.0-beta2

USER root

RUN apt-get update && apt-get -y install -qq --force-yes cron rsyslog

RUN mkdir data
ENV PYCSW_CONFIG=/home/pycsw/data/config.yml

COPY start-cron.sh /usr/local/bin/start-cron.sh
COPY config.yml data/
RUN cd data && /venv/bin/pycsw-admin.py setup-repository --config $PYCSW_CONFIG
COPY harvester /etc/cron.d/harvester
RUN chmod 0644 /etc/cron.d/harvester

ENTRYPOINT [ "/venv/bin/python3", "/usr/local/bin/entrypoint.py" ]
