import json
from MatchaScript import scrape_matchas
from db import store_db

def lambda_handler(event, context):
    try:
        # Scrape matcha data
        matcha_stock = scrape_matchas()

        store_db(matcha_stock)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }