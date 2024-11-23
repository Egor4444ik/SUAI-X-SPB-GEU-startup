import requests, json

client_id = '2423263'
api_key = 'ada677c3-3558-44e5-bb41-d3ed8ad25c15'

url = 'https://api-seller.ozon.ru'

def count_of_goods(method_of_stock='', offer_id='', product_id='', identify_of_stock=None, count_of_stocks=None):
    if method_of_stock == 'FBO':
        url_to_count_of_goods = url + '/v3/product/info/stocks'
        data = {
            "filter": {
                "offer_id": [offer_id] if offer_id else [], #Обработка пустого offer_id
                "product_id": [product_id] if product_id else [], #Обработка пустого product_id
                "visibility": "ALL"
            },
                "last_id": "",
                "limit": 100
        }
    elif method_of_stock in ('FBS', 'rFBS'):
        url_to_count_of_goods = url + '/v1/product/info/stocks-by-warehouse/fbs'
        data = {
            "filter": {
                "offer_id": [offer_id] if offer_id else [], #Обработка пустого offer_id
                "product_id": [product_id] if product_id else [], #Обработка пустого product_id
                "visibility": "ALL",
                "sku": [""] #Заглушка, если sku неизвестен
              },
            "last_id": "",
            "limit": 100
        }
    else:
        if count_of_stocks: # Проверка на None или пустую строку
            url_to_count_of_goods = url + '/v1/product/import/stocks'
            data = {"count_of_stocks": count_of_stocks} #Заполняем count_of_stocks
        elif identify_of_stock: # Проверка на None или пустую строку
            url_to_count_of_goods = url + '/v2/products/stocks' + identify_of_stock
            data = {} # Пустые данные
        else:
            return None #Возвращаем None, если данные некорректны


    return {'url': url_to_count_of_goods, 'data': data}



def take_fullfilment(Client_Id='', Api_key='', Stock_method='', offer_id='', product_id='', identify_of_stock=None, count_of_stocks=None):
    headers = {
        "Client-Id": Client_Id,
        "Api-Key": Api_key,
        "Content-Type": "application/json"
    }
    request_data = count_of_goods(method_of_stock=Stock_method, offer_id=offer_id, product_id=product_id,
                 identify_of_stock=identify_of_stock, count_of_stocks=count_of_stocks)

    if request_data is None:
        return None # Данные некорректны

    try:
        response = requests.post(request_data['url'], headers=headers, json=request_data['data'])
        response.raise_for_status() # Поднимает исключение для не-2xx кодов ответа

        data = response.json()
        return data['result']['total']

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка API Ozon (HTTPError): {e}, код ошибки: {response.status_code}, ответ: {response.text}")
        return None # Возвращаем None при ошибке
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка обработки ответа API Ozon: {e}, ответ: {response.text}")
        return None # Возвращаем None при ошибке
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return None # Возвращаем None при ошибке

print(take_fullfilment(Client_Id=client_id, Api_key=api_key, Stock_method='FBO', offer_id = '123456', product_id = '123456', identify_of_stock = None, count_of_stocks = None))