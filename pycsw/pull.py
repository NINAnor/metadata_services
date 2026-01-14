#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "duckdb==1.4.3",
#   "schedule",
#   "typer",
#   "structlog",
#   "s3fs",
# ]
# ///

import time
import logging
import typer
import duckdb
import schedule
import structlog
import s3fs
from urllib import parse

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


def schedule_updates(csw_path, endpoint_url: str):
    parsed_csw_path = parse.urlparse(csw_path)
    log.info("install extensions")
    conn = duckdb.connect()
    conn.install_extension("httpfs")
    conn.install_extension("sqlite")
    conn.close()

    def check_files():
        fs = s3fs.S3FileSystem(anon=True, endpoint_url=endpoint_url)
        files = fs.glob(f"{parsed_csw_path.netloc}{parsed_csw_path.path}")
        log.info("found:", files=files)

        return set([fs.info(f, refresh=True)["ETag"] for f in files])

    def pull_data():
        log.info("pulling data...")
        conn = duckdb.connect()
        try:
            conn.load_extension("httpfs")
            conn.load_extension("sqlite")

            conn.sql("SET unsafe_disable_etag_checks = true;")
            conn.sql(
                "ATTACH IF NOT EXISTS 'data/records.db' AS sqlite_db (TYPE sqlite);"
            )

            conn.read_parquet(csw_path).to_table("records")

            conn.sql("""
            begin transaction;
            delete from sqlite_db.records where 1 = 1;
            insert into sqlite_db.records by name (
                from records select * exclude (metadata, mcf)
            );
            commit;
            """)
        except Exception as e:
            log.error(e)
        finally:
            conn.close()
        log.info("done")

    def should_pull():
        global etags
        tags_set = check_files()
        if tags_set != etags:
            log.info("tags has changed", old=tags_set, new=etags)
            etags = tags_set
            pull_data()
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
