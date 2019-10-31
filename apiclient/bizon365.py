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
        Получить список страниц регистрации и их рассылок.
        https://blog.bizon365.ru/api/v1/webinars/subpages/#getsubpages
        :param skip:  skip — количество записей, которые нужно пропустить [необязательный параметр]
        :param limit: limit — количество записей, которые нужно получить [необязательный параметр]
        :return: JSON response
        """
        url = 'webinars/subpages/getSubpages?skip={skip}&limit={limit}'.format(skip=skip, limit=limit)
        r = self._client.get(url)
        return r

    def get_list(self, skip: int = 0, limit: int = 50, live: int = 1, auto: int = 1):
        """
        Полученить список доступных отчетов
        https://blog.bizon365.ru/api/v1/webinars/reports/#getlist
        :param skip: пропустить указанное число записей
        :param limit: ограничить количество записей. Не более 100.
        :param live: искать среди живых вебинаров
        :param auto: искать среди автовебинаров
        :return: JSON {
                        name  (строка) идентификатор комнаты. По этому параметру можно определить нужный webinarID.
                        webinarId  (строка) идентификатор вебинара. Этот id используется для получения отчета по вебинару.
                        type (строка) тип вебинара: LiveWebinars или AutoWebinars
                        created (строка, дата в формате ISO) дата создания записи
                        count1 (число) количество участников вебинара
                        count2 (число) длительность вебинара в минутах
                    }
        """
        url = 'webinars/reports/getlist?skip={skip}&limit={limit}&LiveWebinars={live}&AutoWebinars={auto}'.format(
            skip=skip, limit=limit, live=live, auto=auto)
        r = self._client.get(url)
        return r

    def get_webinar_report(self, webinar_id: str):
        """
        Получить отчет по конкретному вебинару
        :param webinar_id: идентификатор вебинара
        :return: JSON
        """
        url = 'webinars/reports/get?webinarId={webinar_id}'.format(webinar_id=webinar_id)
        r = self._client.get(url)
        return r

    def get_webinar_viewers(self, webinar_id: str, skip: int = 0, limit: int = 50):
        """
        Получить список зрителей по конкретному вебинару
        :param webinar_id: идентификатор вебинара
        :param skip: пропустить указанное число записей
        :param limit: ограничить количество записей. Не более 1000.
        :return: JSON
        """
        url = 'webinars/reports/getviewers?webinarId={webinar_id}&skip={skip}&limit={limit}'.format(
            webinar_id=webinar_id, skip=skip, limit=limit)
        r = self._client.get(url)
        return r
