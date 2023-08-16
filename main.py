import asyncio
import logging
from datetime import datetime

from scraper.scraper import scrape

log = logging.getLogger(__name__)


async def schedule():
    log.info("Starting event loop")
    while True:
        asyncio.get_event_loop().create_task(scrape())
        await asyncio.sleep(60 - datetime.now().second + 10)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
    datefmt="%b %d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)

if __name__ == '__main__':
    asyncio.run(schedule())
