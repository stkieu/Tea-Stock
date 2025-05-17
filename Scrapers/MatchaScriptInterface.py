from abc import ABC, abstractmethod
from typing import Dict
from Scrapers.matcha import Matcha
import requests
from bs4 import BeautifulSoup

class MatchaScriptInterface(ABC):
    @classmethod
    @abstractmethod
    def scrape_matchas(self) -> Dict[str, Matcha]:
        pass

    def soupify(self, raw_URL):
        # want to parse the site with the principal matchas
            webpage_response = requests.get(raw_URL)
            webpage = webpage_response.content
            soup = BeautifulSoup(webpage, "html.parser")
            return soup
