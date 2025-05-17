import json
import boto3
from db import store_db
from Dict import BrandDict
from Scrapers.factory import get_scraper

def lambda_handler(event, context):
    try:
        # Scrape matcha data
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('Marukyu')

        all_matcha_data={}

        brand_site_url = [
            (brand, site, url)
            for brand, sites in BrandDict.items()
            for site, url in sites.items()
        ]
        for brand, site, url in brand_site_url: #scraping for all target brands
            scraper = get_scraper(site)
            matcha_stock = scraper.scrape_matchas(url, brand)
            all_matcha_data.update(matcha_stock)

        store_db(all_matcha_data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }