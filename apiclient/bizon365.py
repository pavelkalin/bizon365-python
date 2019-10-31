"""A library that provides a Python interface to the Bizon365 API"""
import requests
from collections import defaultdict
import json
from json.decoder import JSONDecodeError

from typing import Callable, Iterator, Union, Optional, List, Set, Dict, Tuple


class Client:
    """
    Base class which does requests calls
    """
    API_ENDPOINT = 'https://online.bizon365.ru/api/v1/'
    API_KEY = None
    HEADERS = None

    def __init__(self, api_key: str, api_endpoint: str = 'https://online.bizon365.ru/api/v1/'):
        """
        Initialisation
        :param api_endpoint: API url
        :param api_key: API token
        """
        self.API_ENDPOINT = api_endpoint
        self.API_KEY = api_key
        self.HEADERS = {'X-Token': self.API_KEY,
                        'Content-Type': 'application/x-www-form-urlencoded'}

    def get(self, url: str):
        r = requests.get(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.json()

    def post(self, url: str, data: json):
        r = requests.post(self.API_ENDPOINT + url, data=data, headers=self.HEADERS)
        try:
            result = r.json()
        except JSONDecodeError:
            result = r.text
        return result

    def delete(self, url: str, data: json = None):
        if data:
            r = requests.delete(self.API_ENDPOINT + url, data=data, headers=self.HEADERS)
        else:
            r = requests.delete(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.text


class Webinars:
    """
    Class represents webinars section of API
    https://blog.bizon365.ru/api/v1/webinars
    """

    def __init__(self, api_key: str, api_endpoint: str = 'https://online.bizon365.ru/api/v1/'):
        self._client = Client(api_endpoint=api_endpoint, api_key=api_key)

    def get_subpages(self, skip: int = 0, limit: int = 50):
        """
        Получение списка страниц регистрации и их рассылок.
        :param skip:  skip — количество записей, которые нужно пропустить [необязательный параметр]
        :param limit: limit — количество записей, которые нужно получить [необязательный параметр]
        :return: JSON response
        """
        url = 'webinars/subpages/getSubpages?skip={skip}&limit={limit}'.format(skip=skip, limit=limit)
        r = self._client.get(url)
        return r
