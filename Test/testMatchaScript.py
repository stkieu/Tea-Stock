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
import aiohttp


class testMatchaScriptSazen(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def make_mock_response(html_text):
            mock_response = MagicMock()
            mock_response.__aenter__.return_value.text = AsyncMock(return_value=html_text)
            return mock_response
    
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
                <div id = "product-list"></div>
                <div id = "product-list">
                    <div class="product kw-usucha" data-name="Matcha Wako" data-price="0000000071604" data-date="2024-07-20-1604">
                        <div class="product-name"><a href="/en/products/p156-matcha-wako.html">Matcha Wako</a></div>
                    </div>

                    <div class="product kw-usucha" data-name="Matcha Kinrin" data-price="0000000061602" data-date="2024-07-19-1602">
                        <div class="product-name"><a href="/en/products/p155-matcha-kinrin.html">Matcha Kinrin</a></div>
                    </div>
                </div>
            </body>
        </html>
            '''
        URL='https://www.sazentea.com/en/products/c24-marukyu-koyamaen-matcha' #placeholder
        scraper = get_scraper('Sazen')
        scraper_type = scraper()

        #site mssgs
        #want to mock session and get
        out_of_stock = '<strong class="red">This product is unavailable at the moment. Please visit this page again in a few weeks.</strong>'
        in_stock = ''

        mock_get.side_effect = [
            self.make_mock_response(mock_table),
            self.make_mock_response(out_of_stock),
            self.make_mock_response(in_stock)
        ]
   
        
        async with aiohttp.ClientSession() as session:
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Marukyu Koyamaen')

        expected_dict = {
            ('WAKO', 'Sazen'): Matcha (site='Sazen', brand='Marukyu Koyamaen', name = 'WAKO', stock = '0', url = 'https://www.sazentea.com/en/products/p156-matcha-wako.html'),
            ('KINRIN', 'Sazen'): Matcha(site='Sazen', brand='Marukyu Koyamaen', name = 'KINRIN', stock = '1', url =  'https://www.sazentea.com/en/products/p155-matcha-kinrin.html')
        }
        for key in expected_dict:
            self.assertEqual(matcha_dict[key].name, expected_dict[key].name)
            self.assertEqual(matcha_dict[key].url, expected_dict[key].url)
            self.assertEqual(matcha_dict[key].stock, expected_dict[key].stock)    
    
    @patch('aiohttp.ClientSession.get')
    async def test_invalid(self, mock_get):
        invalid_url = 'https://www.sazentea.com/en/products/'
        mock_get.side_effect = aiohttp.ClientError("Invalid URL")
        scraper_type = MatchaScriptSazen()
        async with aiohttp.ClientSession() as session:
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
                <div id = "product-list"></div>
                <div id = "product-list">
                    <div class="product kw-usucha" data-name="Matcha Samidori" data-price="0000000071604" data-date="2024-07-20-1604">
                        <div class="product-name"><a href="/en/products/p825-matcha-samidori.html">Matcha Samidori</a></div>
                    </div>

                    <div class="product kw-usucha" data-name="Matcha Ogurayama" data-price="0000000061602" data-date="2024-07-19-1602">
                        <div class="product-name"><a href="/en/products/p823-matcha-ogurayama.html">Matcha Ogurayama</a></div>
                    </div>
                </div>
            </body>
        </html>
            '''
        
        #site mssgs
        in_stock = ''
        out_of_stock = '<strong class="red">This product is unavailable at the moment. Please visit this page again in a few weeks.</strong>'

        mock_get.side_effect = [
            self.make_mock_response(mock_table),
            self.make_mock_response(in_stock),
            self.make_mock_response(out_of_stock)
        ]

        expected_dict = {
            ('SAMIDORI', 'Sazen') : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'SAMIDORI' , url= 'https://www.sazentea.com/en/products/p825-matcha-samidori.html' , stock= '1'),
            ('OGURAYAMA', 'Sazen') : Matcha(site='Sazen' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.sazentea.com/en/products/p823-matcha-ogurayama.html' , stock= '0')
        }

        URL= 'https://www.sazentea.com/en/products/c85-yamamasa-koyamaen-matcha?srsltid=AfmBOor9vxCm-63u2ZHqd18fHcBzAjRQBWb7_YhSWS97tuabOVb7CG1q' #placeholder
        scraper = get_scraper('Sazen')
        scraper_type = scraper()

        async with aiohttp.ClientSession() as session:
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Yamamasa Koyamaen')
        
        for key in expected_dict:
            self.assertEqual(matcha_dict[key].name, expected_dict[key].name)
            self.assertEqual(matcha_dict[key].url, expected_dict[key].url)
            self.assertEqual(matcha_dict[key].stock, expected_dict[key].stock)

class testMatchaScriptMatchaJP(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def make_mock_response(html_text):
            mock_response = MagicMock()
            mock_response.__aenter__.return_value.text = AsyncMock(return_value=html_text)
            return mock_response
    
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_MatchaJP(self,mock_get):
        mock_table = ''' 
        <html>
            <head>
                <meta property="og:title" content="KOYAMAEN Matcha Powder">
            </head>
            <body>
                <ul class="list-menu list-menu--inline" role="list">
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
                </ul>
            </body>
        </html>
        '''
        URL="https://www.matchajp.net/Koyamaen"
        scraper = get_scraper('MatchaJP')
        scraper_type = scraper()
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
            self.make_mock_response(mock_table),
            self.make_mock_response(in_stock),
            self.make_mock_response(out_of_stock)
        ]

        expected_dict = {
            ('SHIKIBU-NO-MUKASHI', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'SHIKIBU-NO-MUKASHI' , url= 'https://www.matchajp.net/collections/shikibu-no-mukashi' , stock= '1'),
            ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '0')
        }

        async with aiohttp.ClientSession() as session:
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Yamamasa Koyamaen')

        for key in expected_dict:
            self.assertEqual(matcha_dict[key].name, expected_dict[key].name)
            self.assertEqual(matcha_dict[key].url, expected_dict[key].url)
            self.assertEqual(matcha_dict[key].stock, expected_dict[key].stock)

    @patch('aiohttp.ClientSession.get')
    async def test_scrape_MatchaJP_invalid(self,mock_get):
        invalid_url = 'https://www.matchajp.net/INVALID'
        mock_get.side_effect = aiohttp.ClientError("Invalid URL")
        scraper = get_scraper('MatchaJP')
        scraper_type = scraper()
        async with aiohttp.ClientSession() as session:
            result = await scraper_type.scrape_matchas(session, invalid_url, 'Invalid Brand')
        self.assertEqual(result, {})
    
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_MatchaJP_IS(self,mock_get):
        mock_table = ''' 
        <html>
            <head>
                <meta property="og:title" content="KOYAMAEN Matcha Powder">
            </head>
            <body>
                <ul class="list-menu list-menu--inline" role="list">
                    <li>
                        <a href="/collections/koyamaen-matcha-powder" class="mega-menu__link mega-menu__link--level-2 link">
                        YAMAMASA-KOYAMAEN
                        </a>
                        <ul class="list-unstyled" role="list">
                            <li>
                                <a href="/collections/ogurayama" class="mega-menu__link link">
                                OGURAYAMA
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </body>
        </html>
        '''
        #make 3 ogurayama cards with the last one in stock
        list_mock ='''
            <ul class="product-grid">
                <li class="grid__item">
                    <div class="card__badge bottom left"> 
                        <span id="NoMediaStandardBadge-template--15972096409753__product-grid-7625103736985" class="badge badge--bottom-left color-background-1">Sold out</span>
                    </div>
                </li>
                <li class="grid__item">
                    <div class="card__badge bottom left">
                        <span id="NoMediaStandardBadge-template--15972096409753__product-grid-7625103736985" class="badge badge--bottom-left color-background-1">Sold out</span>
                    </div>
                </li>
                <li class="grid__item">
                    <div class="card__badge bottom left"></div>
                </li>
            </ul>
        '''
        mock_get.side_effect = [
            self.make_mock_response(mock_table),
            self.make_mock_response(list_mock)
        ]
        expected_dict = {
            ('OGURAYAMA', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Yamamasa Koyamaen' , name= 'OGURAYAMA' , url= 'https://www.matchajp.net/collections/ogurayama' , stock= '1')
        }
        URL="https://www.matchajp.net/Koyamaen"
        scraper = get_scraper('MatchaJP')
        scraper_type = scraper()
        async with aiohttp.ClientSession() as session:
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Yamamasa Koyamaen')

        for key in expected_dict:
            self.assertEqual(matcha_dict[key].name, expected_dict[key].name)
            self.assertEqual(matcha_dict[key].url, expected_dict[key].url)
            self.assertEqual(matcha_dict[key].stock, expected_dict[key].stock)
    
    @patch('aiohttp.ClientSession.get')
    async def test_scrape_MatchaJP_Hekisuien(self,mock_get):
        mock_table = ''' 
        <html>
            <head>
                <meta property="og:title" content="HEKISUIEN">
            </head>
            <body>
                <ul class="list-menu list-menu--inline" role="list">
                    <li>
                        <a href="/collections/hekisuien" class="mega-menu__link mega-menu__link--level-2 link mega-menu__link--active" aria-current="page">
                            HEKISUIEN
                        </a>
                        <ul class="list-unstyled" role="list">
                            <li>
                                <a href="/collections/shien" class="mega-menu__link link">
                                    SHIEN
                                </a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </body>
        </html>
        '''
    
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
            self.make_mock_response(mock_table),
            self.make_mock_response(out_of_stock)
        ]

        expected_dict = {
            ('SHIEN', 'MatchaJP') : Matcha(site='MatchaJP' , brand= 'Hekisuien' , name= 'SHIEN' , url= 'https://www.matchajp.net/collections/shien' , stock= '0')
        }
        URL="https://www.matchajp.net/Hekisuien"
        scraper = get_scraper('MatchaJP')
        scraper_type = scraper()
        async with aiohttp.ClientSession() as session:
                matcha_dict = await scraper_type.scrape_matchas(session, URL, 'Hekisuien')

        for key in expected_dict:
            self.assertEqual(matcha_dict[key].name, expected_dict[key].name)
            self.assertEqual(matcha_dict[key].url, expected_dict[key].url)
            self.assertEqual(matcha_dict[key].stock, expected_dict[key].stock)

if __name__ == '__main__':
    unittest.main()
