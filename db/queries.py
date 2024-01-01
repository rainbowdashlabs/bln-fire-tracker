from typing import Tuple

import db
from db.db import cursor

import logging

log = logging.getLogger(__name__)


def log_numbers(fires: int, technical: int, rescue: int):
    last = last_nums()
    last_d = last_day()
    o_fire, o_technical, o_rescue = 0, 0, 0
    ld_fire, ld_technical, ld_rescue = 0, 0, 0
    if last:
        o_fire, o_technical, o_rescue = last
    if last:
        ld_fire, ld_technical, ld_rescue = last_d
    d_fires, d_technical, d_rescue = fires - o_fire, technical - o_technical, rescue - o_rescue
    if d_fires < 0:
        d_fires = fires - ld_fire
    if d_technical < 0:
        d_technical = technical - ld_technical
    if d_rescue < 0:
        d_rescue = rescue - ld_rescue
    log.info("Saved to db")
    with cursor() as cur:
        query = """
            INSERT
            INTO calls(fires, technical_assistance, rescue_service)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING"""
        cur.execute(query, [d_fires, d_technical, d_rescue])


def last_nums() -> Tuple[int, int, int] | None:
    query = """
    SELECT
        fires,
        technical_assistance,
        rescue_service
    FROM
        fire_tracker.daily_calls
    WHERE CASE
              WHEN date_trunc('Minutes', now() AT TIME ZONE 'Europe/Berlin') =
                  date_trunc('day', now() AT TIME ZONE 'Europe/Berlin')
                  THEN -- The new day does not start at midnight, but one minute after it
              DAY = ( now() AT TIME ZONE 'Europe/Berlin' - '1 MINUTE'::INTERVAL )::DATE
              ELSE
                  DAY = (now() AT TIME ZONE 'Europe/Berlin')::DATE
    END
    LIMIT 1;"""
    cur: db.pg_cursor
    with cursor() as cur:
        cur.execute(query)
        return cur.fetchone()


def last_day() -> Tuple[int, int, int] | None:
    query = """
    SELECT
        fires,
        technical_assistance,
        rescue_service
    FROM
        fire_tracker.daily_calls
    WHERE
              DAY = ( now() AT TIME ZONE 'Europe/Berlin')::DATE - '1 DAY'::INTERVAL
    END
    LIMIT 1;"""
    cur: db.pg_cursor
    with cursor() as cur:
        cur.execute(query)
        return cur.fetchone()
