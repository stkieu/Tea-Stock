#modified scrape_matchas to take website and table as input to allow for testing using test DB and also allows us the change target brand if we wish
#test cases:
#name,stock, and url should be correctly scraped
#if oos, stock should be oos, not in stock
#if in stock. should be in stock
#test an invalid link -> error handling
from MatchaScript import scrape_matchas
from MatchaScript import Matcha
import requests
import unittest
from unittest.mock import patch, MagicMock

class testMatchaScript(unittest.TestCase):
    
    #https://docs.python.org/3/library/unittest.mock.html we can mock the website to be scraped via unittest mock
    @patch('requests.get')
    def test_scrape(self, mock_get):
        #need to mock matcha site rather than making requests to actual site
        mock_table = '''
        <html>
            <body>
                <table class="principal">
                    <thead><tr><th>Name in<br><strong>Kanji</strong></th><th>Name in<br><strong>Latin characters</strong></th><th><strong>⚫ Koicha<br>⚪ Usucha</strong></th><th><strong>Item Code</strong></th><th>Unit price of<br><strong>20 g CAN</strong></th><th>Unit price of<br><strong>40 g CAN</strong></th><th>Unit price of<br><strong>100 g BAG</strong></th></tr></thead>
                    <tr><td><a href="/en/products/p156-matcha-wako.html">和光</a></td><td><a href="/en/products/p156-matcha-wako.html">WAKO</a></td><td class="center">⚪</td><td><a href="/en/products/p156-matcha-wako.html">MMK006</a></td><td class="r">$14.58</td><td class="r">$25.92</td><td class="r">$58.86</td></tr>  
                    <tr><td><a href="/en/products/p155-matcha-kinrin.html">金輪</a></td><td><a href="/en/products/p155-matcha-kinrin.html">KINRIN</a></td><td class="center">⚫⚪</td><td><a href="/en/products/p155-matcha-kinrin.html">MMK005</a></td><td class="r">$17.28</td><td class="r">$32.40</td><td class="r">-</td></tr>
                </table>
            </body>
        </html>
            '''
        
        #site mssgs
        in_stock = ''
        out_of_stock = '<strong class="red">This product is unavailable at the moment. Please visit this page again in a few weeks.</strong>'

        #need magic mock https://docs.python.org/3/library/unittest.mock.html#magicmock-and-magic-method-support for request
        #mocking sequential request.get calls:
        mock_get.side_effect = [
            MagicMock(content=mock_table.encode('utf-8')),
            MagicMock(content=out_of_stock.encode('utf-8')),  # set wako out of stock
            MagicMock(content=in_stock.encode('utf-8'))  # set kinrin in stock
        ]

        #since we mocked requests.get, the function should return the mocked data rather than the real time data
        site='https://www.sazentea.com/en/products/c24-marukyu-koyamaen-matcha' #placeholder
        matcha_dict = scrape_matchas(site)
        expected_dict = {
            'WAKO': Matcha (name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            'KINRIN': Matcha(name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html')
        }
    
        self.assertEqual(matcha_dict['WAKO'].name, expected_dict['WAKO'].name)
        self.assertEqual(matcha_dict['WAKO'].url, expected_dict['WAKO'].url)
        self.assertEqual(matcha_dict['WAKO'].stock, expected_dict['WAKO'].stock)
        
        self.assertEqual(matcha_dict['KINRIN'].name, expected_dict['KINRIN'].name)
        self.assertEqual(matcha_dict['KINRIN'].url, expected_dict['KINRIN'].url)
        self.assertEqual(matcha_dict['KINRIN'].stock, expected_dict['KINRIN'].stock)
    
    
    @patch('requests.get')
    def test_invalid(self, mock_get):
        invalid_url = 'https://www.sazentea.com/en/products/'
        mock_get.side_effect = requests.exceptions.RequestException("Invalid URL")
        result = scrape_matchas(invalid_url)
        self.assertEqual(result, {})
        



if __name__ == '__main__':
    unittest.main()
