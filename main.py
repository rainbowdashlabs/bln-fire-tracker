import asyncio
import logging
from datetime import datetime

from logformat import configure_logging
from scraper.scraper import scrape

log = logging.getLogger(__name__)


async def schedule():
    log.info("Starting event loop")
    while True:
        asyncio.get_event_loop().create_task(scrape())
        await asyncio.sleep(60 - datetime.now().second + 10)


configure_logging()

if __name__ == '__main__':
    asyncio.run(schedule())
