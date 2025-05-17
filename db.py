import boto3
from botocore.exceptions import ClientError

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html dynamoDB doc
def store_db(matcha_stock, table):
    for matcha_name, matcha_data in matcha_stock.items():
        try:
            #changing to use update_item from boto3 bcs it has conditoinal updates -> more cost efficient so we dont write everytime
            table.update_item(
                Key={"ID": matcha_name},
                UpdateExpression="""
                    SET #url = :url, 
                        #stock = :stock,
                        #site = :site,
                        #brand = :brand
                """, #what we want to be updated and how
                ExpressionAttributeNames={ #map to our table col attr
                    "#url": "url",  
                    "#stock": "stock",
                    "#site" : "site",
                    "#brand" :"brand"
                },
                ExpressionAttributeValues={ #updating with new data
                    ":url": matcha_data.url, 
                    ":stock": matcha_data.stock,
                    ":site" : matcha_data.site,
                    ":brand" : matcha_data.brand
                }
            )
            print(f"Success: {matcha_name}")
        except ClientError as e:
            print(f"Error with {matcha_name}: {e.response['Error']['Message']}")