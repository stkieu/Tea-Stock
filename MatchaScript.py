import requests
from bs4 import BeautifulSoup
from db import store_db

def scrape_matchas():
    # want the site with the principal matchas
    webpage_response = requests.get("https://www.sazentea.com/en/products/c24-marukyu-koyamaen-matcha")
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")

    #get the ul with the matchas
    matcha_types = soup.find(class_="principal") #should be the table
    type_rows = matcha_types.findAll('tr')
    matcha_stock = {}

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
            # Sazen uses strong tag to classify stock
            matcha_stock[matcha_name] = {"stock": "0", "url" : matcha_url}  
        else:
            matcha_stock[matcha_name] = {"stock": "1", "url" : matcha_url}
    
    store_db(matcha_stock)
    
    return matcha_stock

