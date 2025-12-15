load sqlite;

load httpfs;

SET unsafe_disable_etag_checks = true;

ATTACH IF NOT EXISTS 'data/records.db' AS sqlite_db (TYPE sqlite);

delete from sqlite_db.records
where
    1 = 1;

insert into
    sqlite_db.records by name (
        from
            '${CSW_RECORDS_PARQUET_PATH}'
        select
            * exclude (metadata)
    );