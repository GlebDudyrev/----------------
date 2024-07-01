#Импорт библотек
import requests
import json
import pandas as pd
import datetime


def date_request(apikey: str, date: int) -> dict:
    """Функция возвращает значение доллара относительно валют на дату date

    Args:
        apikey (str): Ваш apikey
        date (int): Дата, курс за которую необходим

    Returns:
        dict: Значения доллара на дату
    """
    
    #Отлавливаем ошибку некорректно введенной даты
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print('Некорректная дата')
        return None
    else:
        #Указываем адрес страницы к которой делаем запрос
        url = "https://api.apilayer.com/currency_data/historical"
        #Параметры запроса
        params = {
            'date': date
        }
        #Заголовок
        headers= {
            "apikey": apikey
        }
        #Отправляем запрос
        response = requests.request("GET", url, headers=headers, params=params)
        status_code = response.status_code
        #Если запрос выполнен успешно
        if status_code == 200:
            #То производим десириализацию, создавая словарь
            result = json.loads(response.text)
            #Если результат запроса получен успешно
            if result['success']:
                #То возвращаем значения доллара
                return result['quotes']
            else:
                #Иначе None
                return None
        else:
            #Иначе возвращаем None
            return None
        
        
def get_data_between_dates(apikey: str, start_date: str, end_date: str, n_qoutes: int = 10) -> pd.DataFrame:
    """Возвращает таблицу, строками которой являются даты, а в ячейках значения, доллара на соответствующую дату.

    Args:
        apikey (str): Ваш apikey
        start_date (str): Начальная дата
        end_date (str): Конечная дата
        n_qoutes (int, optional): Количество первых котировок из JSON, которые станут столбцами таблицы. Defaults to 10.

    Returns:
        pd.DataFrame: _description_
    """
    
    try:
        #Превращаем строки в объекты datetime
        datetime_string_format = "%Y-%m-%d"
        start_date = datetime.datetime.strptime(start_date, datetime_string_format)
        end_date = datetime.datetime.strptime(end_date, datetime_string_format)
    except ValueError:
        #Отлавливаем ошибку некорректно введенной даты
        print('Некорректная дата')
        return None
    
    #Список с результатами запросов
    results = []
    dates_list = []
    #Размер шага в днях
    day_delta = datetime.timedelta(days=1)
    #Проверим, что start_date раньше, чем end_date
    if start_date <= end_date:
        #Если ввод корректный, то итерируемся по датам и формируем данные
        for i in range((end_date - start_date).days + 1):
            date = datetime.datetime.strftime(start_date + i * day_delta, datetime_string_format)
            dates_list.append(date)
            qoutes = date_request(apikey, date)
            results.append(qoutes)
        #Формируем нашу таблицу
        data = pd.DataFrame(results, index=dates_list)
        return data.iloc[:, :n_qoutes]
    else:
        #Если ввод некорректный, то отлавливаем ошибку
        raise ValueError('start_date позже, чем end_date')
    
    
if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2022-01-07'
    apikey = 'YOUR API KEY'
    data = get_data_between_dates(apikey, start_date, end_date)
    print(data)