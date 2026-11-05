FROM ghcr.io/prefix-dev/pixi:0.59.0

WORKDIR /pygeoapi

COPY pyproject.toml pixi.lock ./

RUN pixi install --locked

RUN mkdir -p config
COPY local.config.yml config/
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
