import unittest
from parser.Parser import Parser

class ParcerClassTest(unittest.TestCase):

    def test_urlopen(self):
        urlPrefs = {'validator': '',
                     'nameTag': '',
                     'priceTag': '',
                     'measurmentTag': '',
                     'shortDescTag': '',
                     'longDescTag': ''}
        parser = Parser(**urlPrefs)

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_vanna_riho_miami_180_1656309/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_1vanna_riho_miami_180_1656309/'
        result = parser.urlopen(urlToOpen)
        self.assertRaises(UserWarning)

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/gruntovka_starateli_beton_kontakt_20kg/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://www.sdvor.com/moscow/product/mastika-prikleivajuschaja-tehnonikol-no27-22-kg-37678/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)


    def test_urlvalidate(self):
        urlPrefs = {'validator': ['main', {'itemtype': 'http://schema.org/Product'}],
                     'nameTag': '',
                     'priceTag': '',
                     'measurmentTag': '',
                     'shortDescTag': '',
                     'longDescTag': ''}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_vanna_riho_miami_180_1656309/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_1vanna_riho_miami_180_1656309/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/vanny/akrilovye/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['span', {'class': 'span_price'}],
                     'nameTag': '',
                     'priceTag': '',
                     'measurmentTag': '',
                     'shortDescTag': '',
                     'longDescTag': ''}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/gruntovka_starateli_beton_kontakt_20kg/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['h1', {'class': 'container_title'}],
                     'nameTag': '',
                     'priceTag': '',
                     'measurmentTag': '',
                     'shortDescTag': '',
                     'longDescTag': ''}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.sdvor.com/moscow/product/mastika-prikleivajuschaja-tehnonikol-no27-22-kg-37678/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.sdvor.com/moscow/category/obmazochnaja-gidroizoljatsija-5100/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['p', {'class': 'item_price'}],
                     'nameTag': '',
                     'priceTag': '',
                     'measurmentTag': '',
                     'shortDescTag': '',
                     'longDescTag': ''}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.stroyshopper.ru/category/gracia_ceramica_keramogranit/'
        status, result = parser.urlValidate(urlToOpen)
        self.assertFalse(status)
"""
    def test_urlparse(self):
        pass
"""


if __name__ == '__main__':
    unittest.main()
