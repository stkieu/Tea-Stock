#modified scrape_matchas to take website and table as input to allow for testing using test DB and also allows us the change target brand if we wish
#test cases:
#name,stock, and url should be correctly scraped
#if oos, stock should be oos, not in stock
#if in stock. should be in stock
#test an invalid link -> error handling

from Scrapers.MatchaScriptSazen import MatchaScriptSazen
from Scrapers.matcha import Matcha
from Scrapers.factory import get_scraper
import unittest
from unittest.mock import patch, AsyncMock, MagicMock


class testMatchaScriptSazen(unittest.TestCase):
    
    #https://docs.python.org/3/library/unittest.mock.html we can mock the website to be scraped via unittest mock
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_sazen_MK(self, mock_get):
        #need to mock matcha site rather than making requests to actual site
        mock_table = '''
        <html>
            <body>
                <nav id="categorysubmenu" class="en">
                    <div class="submenu-name">Matcha manufacturers:</div>
                    <ul>
                        <li class="active"><a href="/en/products/c24-marukyu-koyamaen-matcha">Marukyu Koyamaen</a></li>
                    </ul
                </nav>
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
            AsyncMock(**{'text.return_value': mock_table}),
            AsyncMock(**{'text.return_value': out_of_stock}),
            AsyncMock(**{'text.return_value': in_stock})
        ]


        #since we mocked requests.get, the function should return the mocked data rather than the real time data
        URL='https://www.sazentea.com/en/products/c24-marukyu-koyamaen-matcha' #placeholder
        scraper_type = get_scraper('Sazen')

        async with patch('aiohttp.ClientSession')() as session:
                session.get = mock_get
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Marukyu Koyamaen')

        expected_dict = {
            'WAKO': Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            'KINRIN': Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html')
        }
    
        self.assertEqual(matcha_dict['WAKO'].name, expected_dict['WAKO'].name)
        self.assertEqual(matcha_dict['WAKO'].url, expected_dict['WAKO'].url)
        self.assertEqual(matcha_dict['WAKO'].stock, expected_dict['WAKO'].stock)
        
        self.assertEqual(matcha_dict['KINRIN'].name, expected_dict['KINRIN'].name)
        self.assertEqual(matcha_dict['KINRIN'].url, expected_dict['KINRIN'].url)
        self.assertEqual(matcha_dict['KINRIN'].stock, expected_dict['KINRIN'].stock)
    
    
    @patch('aiohttp.ClientSession.get')
    async def test_invalid(self, mock_get):
        invalid_url = 'https://www.sazentea.com/en/products/'
        mock_get.side_effect = aiohttp.ClientError("Invalid URL")
        scraper_type = MatchaScriptSazen()
        async with patch('aiohttp.ClientSession')() as session:
            session.get = mock_get
            result = await scraper_type.scrape_matchas(session, invalid_url, 'Invalid Brand')
        self.assertEqual(result, {})

    @patch('aiohttp.ClientSession.get')
    async def test_Sazen_YM(self, mock_get):
        mock_table = '''
        <html>
            <body>
                <nav id="categorysubmenu" class="en">
                    <div class="submenu-name">Matcha manufacturers:</div>
                    <ul>
                       <li class="active"><a href="/en/products/c85-yamamasa-koyamaen-matcha">Yamamasa Koyamaen</a></li>
                    </ul
                </nav>
                <table class="principal">
                <thead><tr><th>Name in<br><strong>Kanji</strong></th><th>Name in<br><strong>Latin characters</strong></th><th><strong>⚫ Koicha<br>⚪ Usucha</strong></th><th><strong>Item Code</strong></th><th>Unit price of<br><strong>30 g CAN</strong></th><th>Unit price of<br><strong>100 g BAG</strong></th><th>Unit price of<br><strong>150 g CAN</strong></th><th>Unit price of<br><strong>300 g CAN</strong></th><th>Unit price of<br><strong>500 g BAG</strong></th><th>Unit price of<br><strong>1000 g BAG</strong></th></tr></thead>
                <tr><td><a href="/en/products/p825-matcha-samidori.html">さみどり</a></td><td><a href="/en/products/p825-matcha-samidori.html">SAMIDORI</a></td><td class="center">⚪</td><td><a href="/en/products/p825-matcha-samidori.html">MYK010</a></td><td class="r">$9.72</td><td class="r">$27.00</td><td class="r">$43.20</td><td class="r">$79.92</td><td class="r">$127.44</td><td class="r">$251.64</td></tr>
                <tr><td><a href="/en/products/p823-matcha-ogurayama.html">小倉山</a></td><td><a href="/en/products/p823-matcha-ogurayama.html">OGURAYAMA</a></td><td class="center">⚪</td><td><a href="/en/products/p823-matcha-ogurayama.html">MYK008</a></td><td class="r">$14.04</td><td class="r">$41.58</td><td class="r">$63.72</td><td class="r">$120.96</td><td class="r">$199.80</td><td class="r">$396.36</td></tr>
                </table>
            </body>
        </html>
            '''
        
        #site mssgs
        in_stock = ''
        out_of_stock = '<strong class="red">This product is unavailable at the moment. Please visit this page again in a few weeks.</strong>'

        mock_get.side_effect = [
            AsyncMock(**{'text.return_value': mock_table}),
            AsyncMock(**{'text.return_value': in_stock}),
            AsyncMock(**{'text.return_value': out_of_stock})
            
        ]

        expected_dict = {
            'SAMIDORI' : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'SAMIDORI' , url= 'https://www.sazentea.com/en/products/p825-matcha-samidori.html' , stock= '1'),
            'OGURAYAMA' : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.sazentea.com/en/products/p823-matcha-ogurayama.html' , stock= '0')
        }

        URL= 'https://www.sazentea.com/en/products/c85-yamamasa-koyamaen-matcha?srsltid=AfmBOor9vxCm-63u2ZHqd18fHcBzAjRQBWb7_YhSWS97tuabOVb7CG1q' #placeholder
        scraper_type = get_scraper('Sazen')
        async with patch('aiohttp.ClientSession')() as session:
                session.get = mock_get
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Yamamasa Koyamaen')

        self.assertEqual(matcha_dict['SAMIDORI'].name, expected_dict['SAMIDORI'].name)
        self.assertEqual(matcha_dict['SAMIDORI'].url, expected_dict['SAMIDORI'].url)
        self.assertEqual(matcha_dict['SAMIDORI'].stock, expected_dict['SAMIDORI'].stock)
        
        self.assertEqual(matcha_dict['OGURAYAMA'].name, expected_dict['OGURAYAMA'].name)
        self.assertEqual(matcha_dict['OGURAYAMA'].url, expected_dict['OGURAYAMA'].url)
        self.assertEqual(matcha_dict['OGURAYAMA'].stock, expected_dict['OGURAYAMA'].stock)

class testMatchaScriptMatchaJP:
     
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_MatchaJP(self,mock_get):
        mock_table = ''' 
        <html>
            <body>
                <li>
                    <a href="/collections/koyamaen-matcha-powder" class="mega-menu__link mega-menu__link--level-2 link">
                    YAMAMASA-KOYAMAEN
                    </a>
                    <ul class="list-unstyled" role="list">
                        <li>
                            <a href="/collections/shikibu-no-mukashi" class="mega-menu__link link">
                            SHIKIBU-NO-MUKASHI
                            </a>
                        </li><li>
                            <a href="/collections/ogurayama" class="mega-menu__link link">
                            OGURAYAMA
                            </a>
                        </li>
                    </ul>
                </li>
            </body>
        </html>
        '''

        #MatchaJP has different links for different sizes upon first size in stock-> update to matcha in stock, stop and provide link to page with the sizes
        #otherwise, if all out of stock, mark OOS
        #card badge bottom left doesnt contain sold out on product card. Just mock one card each
        in_stock ='''
            <ul class="product-grid">
                <li class="grid__item">
                    <div class="card__badge bottom left"></div>
                </li>
            </ul>
        '''
        #html for OOS badge that MatchaJP uses -> card badge bottom left contains sold out on product card
        out_of_stock = '''
            <ul class="product-grid">
                <li class="grid__item">
                    <div class="card__badge bottom left">
                        <span id="NoMediaStandardBadge-template--15972096409753__product-grid-7625103736985" class="badge badge--bottom-left color-background-1">Sold out</span>
                    </div>
                </li>
            </ul>
            
        ''' 
        mock_get.side_effect = [
            AsyncMock(**{'text.return_value': mock_table}),
            AsyncMock(**{'text.return_value': out_of_stock}),
            AsyncMock(**{'text.return_value': in_stock})
        ]

        expected_dict = {
            'SHIKIBU-NO-MUKASHI' : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.matchajp.net/collections/shikibu-no-mukashi' , stock= '1'),
            'OGURAYAMA' : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')
        }

        URL="https://www.matchajp.net/"
        scraper_type = get_scraper('MatchaJP')
        async with patch('aiohttp.ClientSession')() as session:
                session.get = mock_get
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Yamamasa Koyamaen')

        self.assertEqual(matcha_dict['SHIKIBU-NO-MUKASHI'].name, expected_dict['SHIKIBU-NO-MUKASHI'].name)
        self.assertEqual(matcha_dict['SHIKIBU-NO-MUKASHI'].url, expected_dict['SHIKIBU-NO-MUKASHI'].url)
        self.assertEqual(matcha_dict['SHIKIBU-NO-MUKASHI'].stock, expected_dict['SHIKIBU-NO-MUKASHI'].stock)
        
        self.assertEqual(matcha_dict['OGURAYAMA'].name, expected_dict['OGURAYAMA'].name)
        self.assertEqual(matcha_dict['OGURAYAMA'].url, expected_dict['OGURAYAMA'].url)
        self.assertEqual(matcha_dict['OGURAYAMA'].stock, expected_dict['OGURAYAMA'].stock)
     
if __name__ == '__main__':
    unittest.main()
