CREATE TABLE IF NOT EXISTS {schema}.calls
(
    time                 TIMESTAMP         NOT NULL DEFAULT date_trunc('MINUTES', now() AT TIME ZONE 'Europe/Berlin')
        CONSTRAINT calls_pk
            PRIMARY KEY,
    fires                INTEGER DEFAULT 0 NOT NULL,
    technical_assistance INTEGER DEFAULT 0 NOT NULL,
    rescue_service       INTEGER DEFAULT 0 NOT NULL
);

CREATE OR REPLACE VIEW {schema}.daily_calls AS
SELECT time::DATE                AS day,
       sum(fires)                AS fires,
       sum(technical_assistance) AS technical_assistance,
       sum(rescue_service)       AS rescue_service
FROM {schema}.calls
GROUP BY time::DATE;
