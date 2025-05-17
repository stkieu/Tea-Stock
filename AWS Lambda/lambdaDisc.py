#https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html DynamoDB Streams doc
import json
import os 
import boto3
import requests

disc_webhook = os.getenv('disc_webhook')

def lambda_handler(event, context):

    for record in event['Records']:
        if record['eventName'] in ['INSERT', 'MODIFY']:

            new_image = record['dynamodb'].get('NewImage', {})
            old_image = record['dynamodb'].get('OldImage', {})

            new_stock = new_image.get('stock', {}).get('S', '')
            old_stock = old_image.get('stock', {}).get('S', '')

            if old_stock == '0' and new_stock == '1':
                product_ID = new_image.get('ID', {}).get('S', 'Unknown Product') #dynamo struct -> no string detected then return unknown
                url = new_image.get('url', {}).get('S', 'No URL')

                message = {
                    "content": f"**{product_ID}** is now IN STOCK! \nGet it on Sazen: {url}"
                }

                try:
                    response = requests.post(disc_webhook, json=message)
                    response.raise_for_status() 
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
