import json
import boto3
from db import store_db
from Dict.BrandDict import Brands_Dictionary
from Scrapers.factory import get_scraper
from Scrapers import *
import aiohttp
import asyncio

loop = asyncio.get_event_loop() #for Lambda

def lambda_handler(event, context):
    return loop.run_until_complete(async_lambda_handler(event, context))

async def async_lambda_handler(event, context):
    try:
        # Scrape matcha data
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('Marukyu')

        all_matcha_data={}
        # reference: https://www.scrapingbee.com/blog/async-scraping-in-python/#asyncio-featurefunction-overview
        
        brand_site_url = [
            (brand, site, url)
            for brand, sites in Brands_Dictionary.items()
            for site, url in sites.items()
        ]
        async with aiohttp.ClientSession() as session:
            tasks = [] #we want to make these tasks so that we can scrape asynchronously
            for brand, site, url in brand_site_url:
                scraper_type = get_scraper(site)
                scraper = scraper_type()
                task = scraper.scrape_matchas(session, url, brand) #crating coroutine object to schedule
                tasks.append(task)

            results = await asyncio.gather(*tasks) #actual execution of coroutines
            for matcha_stock in results:
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