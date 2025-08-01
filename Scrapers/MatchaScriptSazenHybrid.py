from Scrapers.MatchaScriptInterface import MatchaScriptInterface
from Scrapers.matcha import Matcha
from Dict.Registry import ScraperRegistry
import asyncio

@ScraperRegistry.hybrid_register("SazenHybrid")
class MatchaScriptSazenHybrid(MatchaScriptInterface):
    async def scrape_matchas(self, session, unchecked_products):
        
        try:
            tasks = []
            keys = []

            for (matcha_name, site), matcha_data in unchecked_products.items():
                url = matcha_data.url
                keys.append((matcha_name,site))
                tasks.append(self.soupify(session, url))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            for i, response in enumerate(responses):
                key = keys[i]
                matcha_data = unchecked_products[key]

                if isinstance(response, Exception):
                    print(f"[ERROR] {matcha_data.url}: {response}")
                    continue
                #just from the latter of sazen script
                info = response.find(id="basket-add")

                if info != None:
                    matcha_data.stock = '1'
                else:
                    matcha_data.stock = '0'

            return unchecked_products
        except Exception as e:
            print(f" SazenHybrid Error fetching data: {e}")
            return {}