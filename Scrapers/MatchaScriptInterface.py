from abc import ABC, abstractmethod
from typing import Dict
from Scrapers.matcha import Matcha
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class MatchaScriptInterface(ABC):
    @abstractmethod
    async def scrape_matchas(self, session: aiohttp.ClientSession, *args, **kwargs) -> Dict[str, Matcha]:
        pass

    @retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    retry=retry_if_exception_type(asyncio.TimeoutError)
    )
    async def fetch(self, session, url): #async aiohttp calls to return URL content
        async with session.get(url) as response:
            return await response.text()

    #too many concurrent requests was breaking sazen's site
    semaphore = asyncio.Semaphore(10)
    async def soupify(self,session, raw_URL): 
        async with self.semaphore:
            content = await self.fetch(session, raw_URL)
            return BeautifulSoup(content, "html.parser")
             
