from typing import Tuple

import db
from db.db import cursor

import logging

log = logging.getLogger(__name__)

def log_numbers(fires: int, technical: int, rescue: int):
    last = last_nums()
    o_fire, o_technical, o_rescue = 0, 0, 0
    if last:
        o_fire, o_technical, o_rescue = last
    log.info("Saved to db")
    with cursor() as cur:
        query = """
            INSERT
            INTO calls(fires, technical_assistance, rescue_service)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING"""
        cur.execute(query, [fires - o_fire, technical - o_technical, rescue - o_rescue])


def last_nums() -> Tuple[int, int, int] | None:
    query = """
    SELECT fires,
       technical_assistance,
       rescue_service
    FROM daily_calls
    WHERE day = now()::DATE
    LIMIT 1;"""
    cur: db.pg_cursor
    with cursor() as cur:
        cur.execute(query)
        return cur.fetchone()
