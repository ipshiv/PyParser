import re
from urllib.request import urlopen, Request, URLError, HTTPError


class Parser():

    """
    Common class to parse urls for data extraction
    """

    def __init__(self, **kwargs):
        """
        Data needed to init:
            {'validator': [], - object that should be on a page
             'nameTag': [], - object contains name of material
             'priceTag': [], - object contains price
             'measurmentTag': [], - object contains measurment (if avaible)
             'shortDescTag': [], - object contains short decription (if avaible)
             'longDescTag': []} - object contains long description (if avaible)
        """
        self._validator = kwargs['validator']
        self._nameTag = kwargs['nameTag']
        self._priceTag = kwargs['priceTag']
        self._measurmentTag = kwargs['measurmentTag']
        self._shortDescTag = kwargs['shortDescTag']
        self._longDescTag = kwargs['longDescTag']

    def urlopen(self, url):
        try:
            '''user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            headers = {'User-Agent': user_agent}
            req = Request(url, headers)'''
            response = urlopen(url)
        except URLError:
            raise UserWarning
        except HTTPError:
            raise UserWarning
        else:
            if response.getcode() == 200:
                return response.read().decode('utf-8')
            else:
                raise UserWarning

    def urlValidate(self, url):
        status = False
        rawHTML = None
        try:
            rawHTML = self.urlopen(url)
            # print(rawHTML)
        except UserWarning:
            pass
        else:

            for key, value in self._validator[1].items():
                pattern = r'<%s.*%s="%s"' % (self._validator[0], key, value)
            print(pattern)
            chunk = re.compile(pattern)
            result = chunk.findall(rawHTML)
            if result != []:
                status = True

        return status, rawHTML
