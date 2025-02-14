import requests
from bs4 import BeautifulSoup

class Matcha:
    def __init__(self, name, url, stock):
        self.name = name
        self.url = url
        self.stock = stock

def scrape_matchas(brand):
    try:
        # want the site with the principal matchas
        webpage_response = requests.get(brand)
        webpage = webpage_response.content
        soup = BeautifulSoup(webpage, "html.parser")

        #get the ul with the matchas
        matcha_types = soup.find(class_="principal") #should be the table
        type_rows = matcha_types.findAll('tr')
        matcha_stock = {}
        if not type_rows:
            print("No matcha table found")
            return {}
        
        base_url = "https://www.sazentea.com"
        # each table item
        for matcha in type_rows[1:]:
            matcha_data = matcha.findAll('td')
            matcha_name = matcha_data[1].text.strip()
            matcha_url = base_url+matcha_data[1].find('a')['href']

            web = requests.get(matcha_url)
            webContent = BeautifulSoup(web.content, "html.parser")
            info = webContent.find('strong', class_='red')

            if info:
                stock_info = '0'
            else:
                stock_info = '1'
                
            matcha_obj = Matcha(name=matcha_name, url=matcha_url, stock=stock_info)
            matcha_stock[matcha_name] = matcha_obj
            
        return matcha_stock
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

