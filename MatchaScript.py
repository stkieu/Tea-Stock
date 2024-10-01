import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_matchas():
    # want the site with the principal matchas
    webpage_response = requests.get("https://www.marukyu-koyamaen.co.jp/english/shop/products/category/matcha/principal/")
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")

    #get the ul with the matchas
    matcha_types = soup.find(class_="products")
    matcha_stock = {}

    # each list item
    for matcha in matcha_types.children:
        matcha_name = matcha.find(class_="product-name").h4.text
        classes = matcha.get('class', [])
        # MK uses classes to classify stock
        if 'outofstock' in classes:
            matcha_stock[matcha_name] = "0"
        elif 'instock' in classes:
            matcha_stock[matcha_name] = "1"
    
    return matcha_stock