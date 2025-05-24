from abc import ABC, abstractmethod
from typing import Dict
from Scrapers.matcha import Matcha
from bs4 import BeautifulSoup

class MatchaScriptInterface(ABC):
    @abstractmethod
    def scrape_matchas(self) -> Dict[str, Matcha]:
        pass

    async def fetch(self, session, url): #async aiohttp calls to return URL content
        async with session.get(url) as response:
            return await response.text()
            
    async def soupify(self,session, raw_URL): 
            content = await self.fetch(session, raw_URL)
            return BeautifulSoup(content, "html.parser")
             
