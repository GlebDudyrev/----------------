import requests
import json


def get_search_catalog(query: str, page_num: str) -> list:
    """Возвращает список артикулов товаров, по запросу query, которые находятся на странице page_num

    Args:
        query (str): Запрос в поиске
        page (str): Номер страницы

    Returns:
        list: Список с артикулами
    """
    #Запускаем бесконечный цикл, который закончится, когда будет сформирован верный запрос
    while True:
        #Список с артикулами
        result = []
        #Адрес, к которому будем осуществлять запрос
        url = 'https://search.wb.ru/exactmatch/ru/common/v5/search'
        #Параметры запроса
        params = {
            'query': query,
            'page': page_num,
            'resultset': 'catalog',
            'sort': 'popular',
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-952191',
            'spp': '30',
            'suppressSpellcheck': 'false',
        }
        #Осуществляем запрос
        response = requests.get(url, params=params)
        #Получаем данные и формуруем список
        data = json.loads(response.text)
        for product in data['data']['products']:
            result.append(product['id'])
        #Если список правильный, то возвращаем его
        if len(result) == 100:
            return result


def find_product_position(query: str, id: int) -> tuple:
    """Находит позицию товара

    Args:
        query (str): Запрос в поиске
        id (int): Номер артикула товара

    Returns:
        str: Позиция товара
    """
    #Итерируемся по первым 50-ти страницам
    for page_num in range(1, 51):
        #Получаем каталог со страницы
        id_list = get_search_catalog(query, page_num)
        try:
            #Находим позицию товара на странице
            position = id_list.index(id) + 1
            #Если товар найден возвращаем соответсвующее сообщение
            return f'Товар найден на странице {page_num} на позиции {position}'
        except ValueError:
            #Иначе ничего не делаем
            pass
    #Если товар не найден на первых 50-ти страницах, то сообщаем об этом
    return 'Товар не найден среди первых 50-ти страниц'
            

if __name__ == '__main__':
    result = find_product_position('Платье', 179368512)
    print(result)