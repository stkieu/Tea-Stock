import json
import time
import asyncio
import aiohttp
import aioboto3
from boto3.dynamodb.conditions import Key

from FASTAPI.db import store_db
from Dict.BrandDict import Brands_Dictionary
from Scrapers.factory import get_scraper, get_hybrid_scraper
from Scrapers.matcha import Matcha


loop = asyncio.get_event_loop() #for Lambda

def lambda_handler(event, context):
    return loop.run_until_complete(async_lambda_handler(event, context))

async def scrape_primary_data(brand_site_url, session): #normally scrape site

    start = time.monotonic()
    tasks = [] #we want to make these tasks so that we can scrape asynchronously
    for brand, site, url in brand_site_url:
        scraper_type = get_scraper(site)
        scraper = scraper_type()
        task = scraper.scrape_matchas(session, url, brand) #crating coroutine object to schedule
        tasks.append(task)

    results = await asyncio.gather(*tasks) #actual execution of coroutines
    end = time.monotonic()
    print(f"[TIMING] Primary scrape took {end - start:.2f} sec")

    return results

async def hybrid_difference_helper(table, site, brand, matcha_stock): #gets diff b/w items just scraped and existing db brand,site data
    assert site, "site is None or empty"
    assert brand, "brand is None or empty"
    start = time.monotonic()
    #have to use a GSI for querying, returns all attributes for the items that match query
    response = await table.query(
        IndexName="site-brand-index",
        KeyConditionExpression=Key("site").eq(site) & Key("brand").eq(brand)
    )
    items = response['Items']

    existing_keys = set((item.name, item.site) for item in matcha_stock.values()) #dict w/ Matcha instances

    difference = {
        (item["ID"], item["site"]): item
        for item in items
        if (item["ID"], item["site"]) not in existing_keys
    }
    end = time.monotonic()
    print(f"[TIMING] Difference took {end - start:.2f} sec")
    return difference     

def convert_to_matcha_dict(dynamo_items: dict) -> dict:
    matcha_dict = {}
    for key, item in dynamo_items.items():
        matcha_obj = Matcha(
            site=item["site"],
            brand=item["brand"],
            name=item["ID"],
            url=item["url"],
            stock=item.get("stock", None)
        )
        matcha_dict[key] = matcha_obj
    return matcha_dict

async def hybrid_scrape_data(brand_site_url, primary_results, table, session): #scrape products unchecked by primary
    hybrid_tasks = []
    start = time.monotonic()
    for i in range(len(brand_site_url)):
        
        matcha_stock = primary_results[i]
        if not isinstance(matcha_stock, dict):
            continue

        brand, site, url_ = brand_site_url[i]
        #hybrid scraper might not exist - time efficiency
        try:
            scraper_type = get_hybrid_scraper(site + "Hybrid")
            scraper = scraper_type()
        except ValueError:
            print(f"[HYBRID LOOP] No hybrid scraper for {site}Hybrid")
            continue

        unchecked_products_raw = await hybrid_difference_helper(table, site, brand, matcha_stock)

        #dynamoDB does NOT return matcha obj in the query
        unchecked_products = convert_to_matcha_dict(unchecked_products_raw)

        if unchecked_products and scraper:
            #only need scraper if there are unchecked products
            task = scraper.scrape_matchas(session, unchecked_products) #coroutine
            hybrid_tasks.append(task)

    hybrid_results = await asyncio.gather(*hybrid_tasks) #coroutines execution
    print("Hybrid success")
    end = time.monotonic()
    print(f"[TIMING] Hybrid scrape took {end - start:.2f} sec")
    return hybrid_results

async def async_lambda_handler(event, context):
    try:
        # Scrape matcha data
        start = time.monotonic()
        session = aioboto3.Session()
        
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('Matcha')
            all_matcha_data={}
            # reference: https://www.scrapingbee.com/blog/async-scraping-in-python/#asyncio-featurefunction-overview
            
            brand_site_url = [
                (brand, site, url)
                for brand, sites in Brands_Dictionary.items()
                for site, url in sites.items()
            ]
            
            timeout = aiohttp.ClientTimeout(total=3)
            async with aiohttp.ClientSession(timeout=timeout) as http_session:
                primary_results = await scrape_primary_data(brand_site_url, http_session)
                hybrid_results = await hybrid_scrape_data(brand_site_url, primary_results, table, http_session)

                for matcha_dict in primary_results + hybrid_results:
                    all_matcha_data.update(matcha_dict)
                await store_db(all_matcha_data, table)
            end = time.monotonic()
            print(f"[TIMING] TOTAL {end - start:.2f} sec")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }