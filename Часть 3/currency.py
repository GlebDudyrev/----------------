#Импорт библиотек
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

class Currency():
    def __init__(self, apikey: str) -> None:
        """Метод инициализации

        Args:
            apikey (str): API-ключ для ExchangeRate-API
        """
        #Создаем поле с ключом
        self.key = apikey
        #Создаем поле со списком возможных валют для запроса
        self.get_currency_list()


    def get_currency_rate(self, currency: str) -> str:
        """Возвращает информации о курсе валюты относительно рубля
        
        Args:
            currency (str): Наименование курса валюты

        Returns:
            str: Информация о курсе
        """
        if currency in self.currency_list:
            #Адрес, к которому будем осуществлять запрос
            url = f'https://v6.exchangerate-api.com/v6/{self.key}/pair/{currency}/RUB'
            #Выполняем запрос
            response = requests.get(url)
            #Извлекаем значение курса из запроса
            if response.status_code == 200:
                data = json.loads(response.text)
                if data['result'] == 'success':
                    return '{} - {} RUB'.format(currency, data['conversion_rate'])
        else:
            return 'Некорректный код валюты'


    def get_currency_list(self):
        """Создает поле объекта, которое содержит список с возможными валютами для запроса,
        список создается с помощью информации с официального сайта ExchangeRate-API
        """
        #Адрес, к которому осуществляем запрос
        url = 'https://www.exchangerate-api.com/docs/supported-currencies'
        #Выполняем запрос
        response = requests.get(url)
        #Формируем список с доступными валютами
        page = BeautifulSoup(response.text, 'html.parser')
        table = page.find_all('table')[2]
        currency_list = pd.read_html(str(table))[0].iloc[1:, 0].values
        #Создаем поле для объекта со списками валют
        self.currency_list = currency_list



if __name__ == '__main__':
    currency = Currency('YOUR API KEY')
    print(currency.currency_list)