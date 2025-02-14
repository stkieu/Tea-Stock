#db has one function, store_db. Stores scraped data into dynamoDB table.
#test cases:
#insert new item -> expect new item created
#update only stock -> expect only stock to be updated
#update both stock and URL -> expect both stock and URL to be updated
import unittest
from db import store_db
from MatchaScript import Matcha
import boto3




#use a test database(want integration test that its actually in the table):
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('MatchaTest')
class testDB(unittest.TestCase):
    
    def test_new(self):
        #test dictionary that we would get from MatchaScript
        matcha_stock = {'WAKO': Matcha(name='WAKO', url='https://www.sazentea.com/en/products/p156-matcha-wako.html', stock='0')}
        store_db(matcha_stock, table)

        table_item = table.get_item(Key={'ID':'WAKO'})
        self.assertEqual(table_item['Item'].get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
        self.assertEqual(table_item['Item'].get('stock'), '0')
        #clear DB after we're done
        table.delete_item(
            Key = {
                'ID': 'WAKO'
            }
        )
    def test_stock(self):
        matcha_stock = {'WAKO': Matcha(name='WAKO', url='https://www.sazentea.com/en/products/p156-matcha-wako.html', stock='0')}
        store_db(matcha_stock, table)


        matcha_stock['WAKO'].stock = '1'
        store_db(matcha_stock, table)
        table_item = table.get_item(Key={'ID':'WAKO'})
        self.assertEqual(table_item['Item'].get('stock'), '1')
        table.delete_item(
            Key = {
                'ID': 'WAKO'
            }
        )
    def test_url(self):
        matcha_stock = {'WAKO': Matcha(name='WAKO', url='https://www.sazentea.com/en/products/p155-matcha-kinrin.html', stock='0')}
        store_db(matcha_stock, table)

        matcha_stock['WAKO'].url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'
        matcha_stock['WAKO'].stock = '1'
        store_db(matcha_stock, table)

        table_item = table.get_item(Key={'ID':'WAKO'})
        self.assertEqual(table_item['Item'].get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
        self.assertEqual(table_item['Item'].get('stock'), '1')

        table.delete_item(
        Key = {
            'ID': 'WAKO'
        }
    )


if __name__ == '__main__':
    unittest.main()



    
