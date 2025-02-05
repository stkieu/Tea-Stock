import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('Marukyu')

def store_db(matcha_stock):
    for matcha_name, matcha_data in matcha_stock.items():
        try:
            table.put_item(
                Item={
                    'ID': matcha_name,  
                    'url': matcha_data['url'],  
                    'stock': matcha_data['stock'],  
                }
            )
            print(f"Added: {matcha_name}")
        except ClientError as e:
            print(f"Error with {matcha_name}: {e.response['Error']['Message']}")