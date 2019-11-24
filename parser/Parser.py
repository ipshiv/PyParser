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
        if self._checkdata(kwargs) is True:
            self._validator = kwargs['validator']
            self._nameTag = kwargs['nameTag']
            self._priceTag = kwargs['priceTag']
            self._measurmentTag = kwargs['measurmentTag']
            self._shortDescTag = kwargs['shortDescTag']
            self._longDescTag = kwargs['longDescTag']
        else:
            raise ValueError

    def _checkdata(self, initKwargs):
        dataTypes = ['validator', 'nameTag', 'priceTag', 'measurmentTag', 'shortDescTag', 'longDescTag']
        valid = True
        for type in dataTypes:
            try:
                res = initKwargs[type]
            except KeyError:
                valid = False
            else:
                if isinstance(res, list) is False:
                    valid = False
        return valid

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

    def urlPatternValidate(self, pattern, url):
        status = False
        rawHTML = None
        try:
            rawHTML = self.urlopen(url)
        except UserWarning:
            pass
        else:
            chunk = re.compile(pattern)
            result = chunk.findall(rawHTML)
            if result != []:
                status = True

        return status, rawHTML

    def urlTagValidate(self, tagName, url):
        resPattern = ''
        tag = ''
        prop = ''
        propName = ''
        if tagName == 'validator':
            if self._validator != []:
                tag = self._validator[0]
                for key, value in self._validator[1].items():
                    prop = key
                    propName = value
        elif tagName == 'nameTag':
            if self._nameTag != []:
                tag = self._nameTag[0]
                for key, value in self._nameTag[1].items():
                    prop = key
                    propName = value
        elif tagName == 'priceTag':
            if self._priceTag != []:
                tag = self._priceTag[0]
                for key, value in self._priceTag[1].items():
                    prop = key
                    propName = value
        elif tagName == 'measurmentTag':
            if self._priceTag != []:
                tag = self._priceTag[0]
                for key, value in self._priceTag[1].items():
                    prop = key
                    propName = value
        elif tagName == 'shortDescTag':
            if self._shortDescTag != []:
                tag = self._shortDescTag[0]
                for key, value in self._shortDescTag[1].items():
                    prop = key
                    propName = value
        elif tagName == 'longDescTag':
            if self._longDescTag != []:
                tag = self._longDescTag[0]
                for key, value in self._longDescTag[1].items():
                    prop = key
                    propName = value
        else:
            raise ValueError

        if tag == '':
            raise UserWarning
        else:
            resPattern = r'<%s.*%s="%s"' % (tag, prop, propName)
            return self.urlPatternValidate(resPattern, url)

    def testUniqTag(self, tagName, targetUrls, commonUrls):
        """
            Test tags for uniqness. If tag is only in target urls - tag is uniq and valid
            for scrapping.

            Output:
            retData = {
                'result': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
                'target': {'foundTag': [], 'emptyTag': [], 'errors': []},
                'common': {'foundTag': [], 'emptyTag': [], 'errors': []}
            }
        """
        retData = {
            'result': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
            'target': {'foundTag': [], 'emptyTag': [], 'errors': []},
            'common': {'foundTag': [], 'emptyTag': [], 'errors': []}
        }
        for url in targetUrls:
            status, rawHTML = self.urlTagValidate(tagName, url)
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
            status, rawHTML = self.urlTagValidate(tagName, url)
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
