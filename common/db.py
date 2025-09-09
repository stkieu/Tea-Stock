from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html dynamoDB doc
async def store_db(matcha_stock, table):
    for (matcha_name, site), matcha_data in matcha_stock.items():
        try:
            #changing to use update_item from boto3 bcs it has conditoinal updates -> more cost efficient so we dont write everytime
            await table.update_item(
                Key={ #note these should be immutable
                    "ID": matcha_name,
                    "site": site
                },
                UpdateExpression="""
                    SET #url = :url, 
                        #stock = :stock,
                        #brand = :brand
                """, #what we want to be updated and how
                ExpressionAttributeNames={ #map to our table col attr
                    "#url": "url",  
                    "#stock": "stock",
                    "#brand" :"brand"
                },
                ExpressionAttributeValues={ #updating with new data
                    ":url": matcha_data.url, 
                    ":stock": matcha_data.stock,
                    ":brand" : matcha_data.brand
                }
            )
            print(f"Success: {matcha_name}")
        except ClientError as e:
            print(f"Error with {matcha_name}: {e.response['Error']['Message']}")

#get item for one item, query for multiple
async def db_get_named(ID, table):
    try:
        response = await table.query(KeyConditionExpression = Key('ID').eq(ID))
        return response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    
async def db_get(ID, site, table):
    try:
        response = await table.get_item(Key={'ID': ID, 'site': site})
        return response.get('Item')
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

async def db_get_all(table):
    try:
        items = []
        response = await table.scan()
        items.extend(response['Items'])

        #dynamodb will give LastEvaluatedKey if the scan capped out at 1mb -> starts scanning again from the LEK
        while 'LastEvaluatedKey' in response:
            response = await table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return items
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    
async def db_get_brand(brand, table):
    try:
        response = await table.query(
            IndexName = 'brand-index',
            KeyConditionExpression = Key("brand").eq(brand)
        )
        return response["Items"]
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

async def db_get_site(site,table):
    try:
        response = await table.query(
            IndexName = 'site-index',
            KeyConditionExpression = Key("site").eq(site)
        )
        return response["Items"]
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None