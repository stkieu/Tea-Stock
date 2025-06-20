#db has one function, store_db. Stores scraped data into dynamoDB table.
#test cases:
#insert new item -> expect new item created
#update only stock -> expect only stock to be updated
#update both stock and URL -> expect both stock and URL to be updated
import unittest
import FASTAPI.app.db as db
from Scrapers.matcha import Matcha
import boto3




#use a test database(want integration test that its actually in the table):
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('MatchaTest')
class testDB(unittest.TestCase):
    
    def test_new(self):
        #test dictionary that we would get from MatchaScript
        matcha_stock = {
            ('WAKO', 'Sazen'): Matcha(
            site='Sazen',
            brand='Marukyu Koyamaen',
            name='WAKO',
            url='https://www.sazentea.com/en/products/p156-matcha-wako.html',
            stock='0'
            )
        }
        db.store_db(matcha_stock, table)

        table_item = table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
        item = table_item['Item']
        
        self.assertEqual(item.get('site'), 'Sazen')
        self.assertEqual(item.get('brand'), 'Marukyu Koyamaen')
        self.assertEqual(item.get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
        self.assertEqual(item.get('stock'), '0')
        #clear DB after we're done
        table.delete_item(
            Key = {
                'ID': 'WAKO',
                'site' : 'Sazen'
            }
        )
    def test_stock(self):
        matcha_stock = {
            ('WAKO', 'Sazen'): Matcha(
                site='Sazen', 
                brand='Marukyu Koyamaen', 
                name='WAKO', 
                url='https://www.sazentea.com/en/products/p156-matcha-wako.html', 
                stock='0'
            )
        }
        db.store_db(matcha_stock, table)


        matcha_stock[('WAKO', 'Sazen')].stock = '1'
        db.store_db(matcha_stock, table)
        table_item = table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
        item = table_item['Item']
        self.assertEqual(item.get('stock'), '1')
        table.delete_item(
            Key = {
                'ID': 'WAKO',
                'site' : 'Sazen'
            }
        )
    def test_url(self):
        matcha_stock = {
            ('WAKO', 'Sazen'): Matcha(
                site='Sazen', 
                brand='Marukyu Koyamaen', 
                name='WAKO', 
                url='https://www.sazentea.com/en/products/p155-matcha-kinrin.html', 
                stock='0'
            )
        }
        db.store_db(matcha_stock, table)

        matcha_stock[('WAKO', 'Sazen')].url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'
        matcha_stock[('WAKO', 'Sazen')].stock = '1'
        db.store_db(matcha_stock, table)

        table_item = table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
        item = table_item['Item']
        self.assertEqual(item.get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
        self.assertEqual(item.get('stock'), '1')

        table.delete_item(
        Key = {
            'ID': 'WAKO',
            'site':'Sazen'
        }
    )
    
    #test single getting
    def test_get(self):
        matcha_stock = {
            ('WAKO', 'Sazen'): Matcha(
                site='Sazen', 
                brand='Marukyu Koyamaen', 
                name='WAKO', 
                url='https://www.sazentea.com/en/products/p156-matcha-wako.html', 
                stock='0'
            )
        }
        db.store_db(matcha_stock, table)

        item = db.db_get('WAKO', 'Sazen', table)
        expected = {
            'ID': 'WAKO',
            'site': 'Sazen',
            'brand': 'Marukyu Koyamaen',
            'url': 'https://www.sazentea.com/en/products/p156-matcha-wako.html',
            'stock': '0'
        }
        self.assertEqual(item, expected)
        table.delete_item(
            Key = {
                'ID': 'WAKO',
                'site':'Sazen'
            }
        )
#test ID get
    def test_get_named(self):
        mock_dict = {
                ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
                ('WAKO', 'MatchaJP'): Matcha (site='MatchaJP', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.matchajp.net/collections/wako'),
        }

        expected_dict = {
                ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                ('WAKO', 'MatchaJP'): Matcha (site='MatchaJP', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.matchajp.net/collections/wako')
        }

        db.store_db(mock_dict, table)
        items = db.db_get_named('WAKO', table)
        result_dict = {
                (item['ID'], item['site']): Matcha(
                    site=item['site'],
                    brand=item['brand'],
                    name=item['ID'],
                    url=item['url'],
                    stock=item['stock']
                )
                for item in items
            }
        for key in expected_dict:
            actual = result_dict.get(key)
            expected = expected_dict[key]
            
            self.assertEqual(actual.site, expected.site)
            self.assertEqual(actual.brand, expected.brand)
            self.assertEqual(actual.name, expected.name)
            self.assertEqual(actual.url, expected.url)
            self.assertEqual(actual.stock, expected.stock)
            table.delete_item(
                Key = {
                    'ID': actual.name,
                    'site':actual.site
                }
            )

#test brand get
    def test_get_brand(self):
        mock_dict = {
            ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
            ('SHIKIBU-NO-MUKASHI', 'Sazen') : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.sazentea.com/en/products/p822-matcha-shikibu-no-mukashi.html' , stock= '1'),
            ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')        
        }

        expected_dict = {
            ('SHIKIBU-NO-MUKASHI', 'Sazen') : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.sazentea.com/en/products/p822-matcha-shikibu-no-mukashi.html' , stock= '1'),
            ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')
        }

        db.store_db(mock_dict, table)
        items = db.db_get_brand('Yamamasa Koyamaen', table)

        result_dict = {
            (item['ID'], item['site']): Matcha(
                site=item['site'],
                brand=item['brand'],
                name=item['ID'],
                url=item['url'],
                stock=item['stock']
            )
            for item in items
        }
        for key in expected_dict:
            actual = result_dict.get(key)
            expected = expected_dict[key]
            
            self.assertEqual(actual.site, expected.site)
            self.assertEqual(actual.brand, expected.brand)
            self.assertEqual(actual.name, expected.name)
            self.assertEqual(actual.url, expected.url)
            self.assertEqual(actual.stock, expected.stock)
            table.delete_item(
                Key = {
                    'ID': actual.name,
                    'site':actual.site
                }
            )

#test site get
    def test_get_site(self):
        mock_dict = {
            ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
            ('SHIKIBU-NO-MUKASHI', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.matchajp.net/collections/shikibu-no-mukashi' , stock= '1'),
            ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')        
        }

        expected_dict = {
            ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html')    }

        db.store_db(mock_dict, table)
        items = db.db_get_site('Sazen', table)

        result_dict = {
            (item['ID'], item['site']): Matcha(
                site=item['site'],
                brand=item['brand'],
                name=item['ID'],
                url=item['url'],
                stock=item['stock']
            )
            for item in items
        }
        for key in expected_dict:
            actual = result_dict.get(key)
            expected = expected_dict[key]
            
            self.assertEqual(actual.site, expected.site)
            self.assertEqual(actual.brand, expected.brand)
            self.assertEqual(actual.name, expected.name)
            self.assertEqual(actual.url, expected.url)
            self.assertEqual(actual.stock, expected.stock)
            table.delete_item(
                Key = {
                    'ID': actual.name,
                    'site':actual.site
                }
            )
if __name__ == '__main__':
    unittest.main()



    
