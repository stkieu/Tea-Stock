from Scrapers.MatchaScriptInterface import MatchaScriptInterface
from Scrapers.matcha import Matcha
from Dict.Registry import ScraperRegistry
import asyncio

@ScraperRegistry.register("Sazen")
class MatchaScriptSazen(MatchaScriptInterface):
    

    async def scrape_matchas(self, session, raw_URL, brand):  #'async' marks the method as a coroutine, pass in session from lambda (more efficient)
        try:
            soup = await self.soupify(session, raw_URL)
            # print(soup.prettify())
            #get the ul with the matchas
            matcha_types = soup.findAll(id="product-list") #should be div containing 1 div per item update: sazen is using duplicate ids? idex to work around
            if not matcha_types:
                print("No Matcha found")
                return{}
            matcha_stock = {}

            base_url = "https://www.sazentea.com"
            matcha_site = "Sazen"
            matcha_brand = brand

            for matcha in matcha_types[1].find_all("div", recursive=False): #want to be accessing each div child of the product list (want product not bestseller list hence index 1)
                raw_name = matcha.find(class_="product-name").text
                parts = raw_name.split()

                if len(parts) > 1:
                    rest = " ".join(parts[1:])
                    matcha_name = rest.upper()
                else:
                    matcha_name = ""
                    
                matcha_url = base_url+matcha.find('a')['href']

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