import json
import boto3
from db import store_db
from Dict.BrandDict import Brands_Dictionary
from Dict.Registry import ScraperRegistry
from Scrapers.factory import get_scraper
from Scrapers import *

def lambda_handler(event, context):
    try:
        # Scrape matcha data
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('Marukyu')

        all_matcha_data={}

        brand_site_url = [
            (brand, site, url)
            for brand, sites in Brands_Dictionary.items()
            for site, url in sites.items()
        ]
        for brand, site, url in brand_site_url: #scraping for all target brands
            scraper_type = get_scraper(site)
            scraper = scraper_type()
            matcha_stock = scraper.scrape_matchas(url, brand)
            all_matcha_data.update(matcha_stock)

        store_db(all_matcha_data, table)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }