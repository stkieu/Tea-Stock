import json
from MatchaScript import scrape_matchas
import boto3
from db import store_db

def lambda_handler(event, context):
    try:
        # Scrape matcha data
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('Marukyu') 
        brand = 'https://www.sazentea.com/en/products/c24-marukyu-koyamaen-matcha'  
        matcha_stock = scrape_matchas(brand)

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