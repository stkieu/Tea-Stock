import json
import boto3


dynamodb = boto3.resource('dynamodb') 
table = dynamodb.Table('Marukyu')  #connect to db

def lambda_handler(event, context):
    try:
        
        response = table.scan()  
        items = response['Items']
        
        return {
            'body': json.dumps(items)
        }
        
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }