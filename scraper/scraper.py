import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from db import queries

log = logging.getLogger(__name__)


async def scrape():
    headers = {
        # "Accept-Type": "*/*",
        # "Accept-Encoding": "gzip, br, deflate",
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Referer": "https://www.berliner-feuerwehr.de/",
        # "Accept-Language": "en-US,en;q=0.5",
        "X-Requested-With": "XMLHttpRequest",
        # "Content-Type": "text/html; charset=UTF-8"
    }
    async with ClientSession(headers=headers) as session:
        response = await session.get("https://www.berliner-feuerwehr.de/typo3conf/bfw/fireData.php")
        html = await response.text()
        soup = BeautifulSoup(html, features="html.parser")
        log.info(soup.find(attrs={"class": "title"}).text)
        numbers = [int(e.text) for e in soup.find_all(attrs={"class": "textfigure"})]
        for e in zip(numbers, ["Brandbekämpfungen", "Technische Hilfeleistungen", "Rettungsdiensteinsätze"]):
            log.info(f"{e[0]}: {e[1]}")

        queries.log_numbers(*numbers)
