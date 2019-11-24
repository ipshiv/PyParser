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
            chunk = re.compile(pattern)
            result = chunk.findall(rawHTML)
            if result != []:
                status = True

        return status, rawHTML

    def testValidationTags(self, targetUrls, commonUrls):
        retData = {
            'result': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
            'target': {'foundTag': [], 'emptyTag': [], 'errors': []},
            'common': {'foundTag': [], 'emptyTag': [], 'errors': []}
        }
        for url in targetUrls:
            status, rawHTML = self.urlValidate(url)
            if status is True:
                retData['result']['TP'] += 1
                retData['target']['foundTag'].append(url)
            elif status is False and rawHTML is not None:
                retData['result']['FN'] += 1
                retData['target']['emptyTag'].append(url)
            else:
                # print(url)
                retData['target']['errors'].append(url)

        for url in commonUrls:
            status, rawHTML = self.urlValidate(url)
            if status is True:
                retData['result']['FP'] += 1
                retData['common']['foundTag'].append(url)
            elif status is False and rawHTML is not None:
                retData['result']['TN'] += 1
                retData['common']['emptyTag'].append(url)
            else:
                # print(url)
                retData['common']['errors'].append(url)

        return retData
