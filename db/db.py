import contextlib
import json
import logging
from pathlib import Path
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor as pg_cursor
from pydantic import BaseModel

log = logging.getLogger(__name__)


class Configuration(BaseModel):
    host: str = "localhost"
    database: str = "postgres"
    port: int = 5432
    user: str = "postgres"
    password: str = "root"
    db_schema: str = "fire_tracker"


config_path = Path("config/database.json")
if not config_path.exists():
    config_path.parent.mkdir(parents=True)
    config_path.open("w").write(Configuration().model_dump_json(indent=2))

config = Configuration(**json.loads(config_path.open("r").read()))

print(config.model_dump_json())


@contextlib.contextmanager
def connection(host=config.host, user=config.user,
               passwd=config.password, dbname=config.database):
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=passwd,
        dbname=dbname,
        options=f"-c search_path={config.db_schema}")
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def cursor(host=config.host, user=config.user,
           passwd=config.password, dbname=config.database) -> Generator[pg_cursor, None, None]:
    with connection(host, user, passwd, dbname) as conn:
        cur: pg_cursor = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()


def setup():
    with cursor() as cur:
        with open("schema.sql", "r") as f:
            log.info("Setting up database")
            cur.execute(str(f.read()).format_map({"schema": config.db_schema}))


setup()
