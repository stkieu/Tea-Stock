from Scrapers.MatchaScriptInterface import MatchaScriptInterface
from Scrapers.matcha import Matcha
from Dict.Registry import ScraperRegistry
import asyncio

@ScraperRegistry.register("Sazen")
class MatchaScriptSazen(MatchaScriptInterface):
    

    async def scrape_matchas(self, session, raw_URL, brand):  #'async' marks the method as a coroutine, pass in session from lambda (more efficient)
        try:
            soup = await self.soupify(session, raw_URL)
            #get the ul with the matchas
            matcha_types = soup.find(class_="principal") #should be the table
            type_rows = matcha_types.findAll('tr')
            matcha_stock = {}
            if not type_rows:
                print("No matcha table found")
                return {}
            
            base_url = "https://www.sazentea.com"
            matcha_site = "Sazen"
            matcha_brand = brand
            # each table item
            for matcha in type_rows[1:]:
                matcha_data = matcha.findAll('td')
                matcha_name = matcha_data[1].text.strip()
                matcha_url = base_url+matcha_data[1].find('a')['href']

                webContent = await self.soupify(session, matcha_url)
                info = webContent.find('strong', class_='red')

                if info == None:
                    stock_info = '1'
                else:
                    stock_info = '0'
                    
                matcha_obj = Matcha(site=matcha_site, brand= matcha_brand, name=matcha_name, url=matcha_url, stock=stock_info)
                matcha_stock[(matcha_name, matcha_site)] = matcha_obj

            return matcha_stock
        except Exception as e:
            print(f"Error fetching data: {e}")
            return {}