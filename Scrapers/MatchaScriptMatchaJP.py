import asyncio
from .MatchaScriptInterface import MatchaScriptInterface
from .matcha import Matcha
from Dict.Registry import ScraperRegistry

@ScraperRegistry.register("MatchaJP")
class MatchaScriptMatchaJP(MatchaScriptInterface):
    def find_brand(self, matcha_menu, matcha_brand):
        brand_types = None
        for a_tag in matcha_menu.find_all('a'):
                if a_tag.get_text(strip=True) == matcha_brand:
                    brand_types = a_tag
                    break
        return brand_types
        
    async def scrape_matchas(self, session, raw_URL, brand):
        try:
            soup = await self.soupify(session, raw_URL)

            matcha_brand = soup.find('meta', property='og:title')['content'].split()[0]
            if matcha_brand == 'KOYAMAEN':
                matcha_brand = 'YAMAMASA-KOYAMAEN'

            matcha_site = 'MatchaJP'
            matcha_menu = soup.find(class_="list-menu list-menu--inline") #ALL matcha menu
            brand_types = self.find_brand(matcha_menu, matcha_brand) #brand location in menu
            if brand_types is None:
                raise ValueError(f"Brand '{matcha_brand}' not found in menu.")
            
            brand_types_parent = brand_types.parent
            matcha_types = brand_types_parent.find(class_ = 'list-unstyled').find_all('li', recursive=False) #should be list of brand matcha names

            base_url = "https://www.matchajp.net"
            matcha_stock = {}
            for matcha in matcha_types: #access each matcha name in the brand list
                matcha_name = matcha.find('a').text.strip()
                matcha_url = base_url+ matcha.find('a')['href']

                webContent = await self.soupify(session, matcha_url)
                info = webContent.find(class_ = 'product-grid')
                
                
                if info: #iterate through each size(has separate links)
                    product_cards = info.find_all('li', class_ = "grid__item")
                    
                    for card in product_cards:
                        badge = card.find("div", class_="card__badge")
                        if badge.text.strip() == "Sold out":
                            stock_info = '0'  # out of stock
                        else:
                            stock_info = '1'  # in stock
                            break #break only when we find one in stock otherwise continue checking
                matcha_obj = Matcha(site=matcha_site, brand= brand, name=matcha_name, url=matcha_url, stock=stock_info)
                matcha_stock[matcha_name] = matcha_obj

            return matcha_stock
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            return {}