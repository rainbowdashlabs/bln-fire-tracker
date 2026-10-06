import json
import logging
import os
import sys
from datetime import datetime, timezone


class EcsJsonFormatter(logging.Formatter):
    """Formats each record as one line of JSON using Elastic Common Schema field names."""

    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "@timestamp": datetime.fromtimestamp(record.created, timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "log.level": record.levelname,
            "log.logger": record.name,
            "message": record.getMessage(),
            "process.thread.name": record.threadName,
        }
        if record.exc_info:
            error_type, error, _ = record.exc_info
            entry["error.type"] = error_type.__qualname__ if error_type else None
            entry["error.message"] = str(error)
            entry["error.stack_trace"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False, default=str)


def configure_logging():
    """Logs at DEBUG in the readable format, or as ECS JSON on stdout when LOG_FORMAT=json."""
    if os.getenv("LOG_FORMAT", "").lower() == "json":
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(EcsJsonFormatter())
    else:
        handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%b %d %H:%M:%S",
        handlers=[handler]
    )
