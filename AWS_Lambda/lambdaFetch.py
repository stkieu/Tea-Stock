import json
import boto3


dynamodb = boto3.resource('dynamodb') 
table = dynamodb.Table('Matcha')  #connect to db

def lambda_handler(event, context):
    try:
        
        response = table.scan()  
        items = response['Items']
        
        
        formatted_items = {}
        for item in items:
            
            formatted_items[item['ID']] = {
                'url': item['url'],
                'stock': item['stock']
        }
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
        
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }