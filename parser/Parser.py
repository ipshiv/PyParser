#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import ssl
from urllib.request import urlopen, Request, URLError, HTTPError
from http.client import InvalidURL
from bs4 import BeautifulSoup


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
        self.__dataTypes = ['validator', 'nameTag', 'priceTag', 'measurmentTag', 'shortDescTag', 'longDescTag']
        if self._checkdata(kwargs) is True:
            self._tags = kwargs
        else:
            raise ValueError

    def _checkdata(self, initKwargs):
        valid = True
        for type in self.__dataTypes:
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
            req = Request(url, headers)
            gcontext = ssl.SSLContext()'''
            # print(url, end=" ")
            response = urlopen(url)
        except URLError as err:
            print(err.msg)
            raise UserWarning
        except HTTPError as err:
            print(err.msg)
            raise UserWarning
        except ConnectionResetError as err:
            print(err.msg)
            raise UserWarning
        except InvalidURL as err:
            print(err)
            raise UserWarning
        except ValueError as err:
            print(err)
            raise UserWarning
        else:
            # print(response.getcode())
            if response.getcode() == 200:
                return response.read().decode('utf-8', errors="ignore")
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
        try:
            tag, props = self._tags[tagName]
        except KeyError:
            raise ValueError
        else:
            if tag == '':
                raise UserWarning
            else:
                for key, value in props.items():
                    prop = key
                    propName = value
                resPattern = r'<%s' % tag
                if prop != '':
                    resPattern = resPattern + r'.*%s' % prop
                    if propName != '':
                        resPattern = resPattern + r'="%s"' % propName
                    else:
                        resPattern = resPattern + r'=""'
                return self.urlPatternValidate(resPattern, url)

    def testUniqTag(self, tagName, targetUrls, commonUrls=[]):
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

    def parseUrl(self, url):
        retData = {'name': '',
                   'price': '',
                   'measurment': '',
                   'shortDesc': '',
                   'longDesc': '',
                   'url': ''}
        validator = self.__dataTypes[0]
        status, html = self.urlTagValidate(validator, url)
        if status is True:
            print(url, status)
            soup = BeautifulSoup(html, 'html.parser')
            for type in self.__dataTypes[1:]:
                if self._tags[type][0] != '':
                    retData[type.replace('Tag', '')] = soup.find(self._tags[type][0], self._tags[type][1]).get_text().strip()
            retData['url'] = url

        return retData
