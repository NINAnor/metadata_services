import json

import yaml
import pathlib
import s3fs
import environ
import typer
import logging
import structlog
import schedule
import time
from pygeoapi.openapi import generate_openapi_document

env = environ.Env()

S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
S3_BUCKET = env("S3_BUCKET")
S3_PATH = env("S3_PATH", default="/geoapi/*.json")


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

log = structlog.get_logger()

etags: set[str] = set()


def schedule_updates(
    geoapi_path: str = f"{S3_BUCKET}/{S3_PATH}",
    endpoint_url: str = S3_ENDPOINT_URL,
    output_folder: str = "",
):
    log.info("using variables", geoapi_path=geoapi_path, endpoint_url=endpoint_url)
    fs = s3fs.S3FileSystem(anon=True, endpoint_url=endpoint_url)

    def check_files():
        files = fs.glob(geoapi_path)
        log.info("found:", files=files)

        return set([fs.info(f, refresh=True)["ETag"] for f in files])

    def pull_data():
        log.info("pulling data...")
        base_config = yaml.load(pathlib.Path("base.yml").open(), yaml.SafeLoader)

        resources = {}

        for resource_file in fs.glob(geoapi_path):
            for resource in json.loads(fs.open(resource_file).read()):
                resources[resource["id"]] = resource

        base_config["resources"] = resources

        output_path = pathlib.Path(output_folder)
        log.info("writing config")
        yaml.dump(
            base_config, (output_path / "local.config.yml").open("w"), yaml.SafeDumper
        )

        log.info("writing openapi")
        with (pathlib.Path(output_path) / "local.openapi.yml").open(mode="w") as f:
            f.write(
                generate_openapi_document(
                    (output_path / "local.config.yml"),
                    output_format="yaml",  # ty:ignore[invalid-argument-type]
                    fail_on_invalid_collection=True,
                )
            )
        log.info("done")

    def should_pull():
        global etags
        tags_set = check_files()
        if tags_set != etags:
            log.info("tags has changed", old=tags_set, new=etags)
            try:
                etags = tags_set
                pull_data()
            except Exception as e:
                log.error(e)
        else:
            log.info("No changes, skip")

    log.info("first pull")
    should_pull()

    schedule.every().minutes.do(should_pull)
    log.info("starting scheduler")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    typer.run(schedule_updates)
