#db has one function, store_db. Stores scraped data into dynamoDB table.
#test cases:
#insert new item -> expect new item created
#update only stock -> expect only stock to be updated
#update both stock and URL -> expect both stock and URL to be updated
import unittest
import common.db as db
from Scrapers.matcha import Matcha
import aioboto3
import boto3




#use a test database(want integration test that its actually in the table):
class testDB(unittest.IsolatedAsyncioTestCase):
    
    async def test_new(self):
        #test dictionary that we would get from MatchaScript
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            matcha_stock = {
                ('WAKO', 'Sazen'): Matcha(
                site='Sazen',
                brand='Marukyu Koyamaen',
                name='WAKO',
                url='https://www.sazentea.com/en/products/p156-matcha-wako.html',
                stock='0'
                )
            }
            await db.store_db(matcha_stock, table)

            table_item = await table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
            item = table_item['Item']
            
            self.assertEqual(item.get('site'), 'Sazen')
            self.assertEqual(item.get('brand'), 'Marukyu Koyamaen')
            self.assertEqual(item.get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
            self.assertEqual(item.get('stock'), '0')
            #clear DB after we're done
            await table.delete_item(
                Key = {
                    'ID': 'WAKO',
                    'site' : 'Sazen'
                }
            )
    async def test_stock(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            matcha_stock = {
                ('WAKO', 'Sazen'): Matcha(
                    site='Sazen', 
                    brand='Marukyu Koyamaen', 
                    name='WAKO', 
                    url='https://www.sazentea.com/en/products/p156-matcha-wako.html', 
                    stock='0'
                )
            }
            await db.store_db(matcha_stock, table)


            matcha_stock[('WAKO', 'Sazen')].stock = '1'
            await db.store_db(matcha_stock, table)
            table_item = await table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
            item = table_item['Item']
            self.assertEqual(item.get('stock'), '1')
            await table.delete_item(
                Key = {
                    'ID': 'WAKO',
                    'site' : 'Sazen'
                }
            )
    async def test_url(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            matcha_stock = {
                ('WAKO', 'Sazen'): Matcha(
                    site='Sazen', 
                    brand='Marukyu Koyamaen', 
                    name='WAKO', 
                    url='https://www.sazentea.com/en/products/p155-matcha-kinrin.html', 
                    stock='0'
                )
            }
            await db.store_db(matcha_stock, table)

            matcha_stock[('WAKO', 'Sazen')].url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'
            matcha_stock[('WAKO', 'Sazen')].stock = '1'
            await db.store_db(matcha_stock, table)

            table_item = await table.get_item(Key={'ID':'WAKO' , 'site':'Sazen'})
            item = table_item['Item']
            self.assertEqual(item.get('url'), 'https://www.sazentea.com/en/products/p156-matcha-wako.html')
            self.assertEqual(item.get('stock'), '1')

            await table.delete_item(
            Key = {
                'ID': 'WAKO',
                'site':'Sazen'
            }
    )
    

class testDbREST(unittest.IsolatedAsyncioTestCase):
    async def test_get(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            matcha_stock = {
                ('WAKO', 'Sazen'): Matcha(
                    site='Sazen', 
                    brand='Marukyu Koyamaen', 
                    name='WAKO', 
                    url='https://www.sazentea.com/en/products/p156-matcha-wako.html', 
                    stock='0'
                )
            }
            await db.store_db(matcha_stock, table)

            item = await db.db_get('WAKO', 'Sazen', table)
            expected = {
                'ID': 'WAKO',
                'site': 'Sazen',
                'brand': 'Marukyu Koyamaen',
                'url': 'https://www.sazentea.com/en/products/p156-matcha-wako.html',
                'stock': '0'
            }
            self.assertEqual(item, expected)
            await table.delete_item(
                Key = {
                    'ID': 'WAKO',
                    'site':'Sazen'
                }
            )
#test ID get
    async def test_get_named(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            mock_dict = {
                    ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                    ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
                    ('WAKO', 'MatchaJP'): Matcha (site='MatchaJP', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.matchajp.net/collections/wako'),
            }

            expected_dict = {
                    ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                    ('WAKO', 'MatchaJP'): Matcha (site='MatchaJP', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.matchajp.net/collections/wako')
            }

            await db.store_db(mock_dict, table)
            items = await db.db_get_named('WAKO', table)
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
                await table.delete_item(
                    Key = {
                        'ID': actual.name,
                        'site':actual.site
                    }
                )

#test get all
    async def test_get_all(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            mock_dict = {
                ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
                ('SHIKIBU-NO-MUKASHI', 'Sazen') : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.sazentea.com/en/products/p822-matcha-shikibu-no-mukashi.html' , stock= '1'),
                ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')        
            }
            
            await db.store_db(mock_dict, table)
            items = await db.db_get_all(table)
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
            for key in mock_dict:
                actual = result_dict.get(key)
                expected = mock_dict[key]
                
                self.assertEqual(actual.site, expected.site)
                self.assertEqual(actual.brand, expected.brand)
                self.assertEqual(actual.name, expected.name)
                self.assertEqual(actual.url, expected.url)
                self.assertEqual(actual.stock, expected.stock)
                await table.delete_item(
                    Key = {
                        'ID': actual.name,
                        'site':actual.site
                    }
                )

#test brand get
    async def test_get_brand(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
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

            await db.store_db(mock_dict, table)
            items = await db.db_get_brand('Yamamasa Koyamaen', table)

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
                await table.delete_item(
                    Key = {
                        'ID': actual.name,
                        'site':actual.site
                    }
                )

#test site get
    async def test_get_site(self):
        session = aioboto3.Session()
        async with session.resource("dynamodb", region_name="us-west-2") as dynamodb:

            table = await dynamodb.Table('MatchaTest')
            mock_dict = {
                ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html'),
                ('SHIKIBU-NO-MUKASHI', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.matchajp.net/collections/shikibu-no-mukashi' , stock= '1'),
                ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')        
            }

            expected_dict = {
                ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
                ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html')    }

            await db.store_db(mock_dict, table)
            items = await db.db_get_site('Sazen', table)

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
                await table.delete_item(
                    Key = {
                        'ID': actual.name,
                        'site':actual.site
                    }
                )
if __name__ == '__main__':
    unittest.main()



    
