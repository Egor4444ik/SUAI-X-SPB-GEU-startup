import requests

client_id = '2423263'
api_key = 'ada677c3-3558-44e5-bb41-d3ed8ad25c15'

url = 'https://api-seller.ozon.ru'

method_of_stock = ['FBO']
count_of_stocks = 1

if count_of_stocks == 1:
    identify_of_stock = None

else:
    identify_of_stock = str

def count_of_goods(method_of_stock, identify_of_stock, count_of_stocks):

    if method_of_stock == 'FBO':
        url_to_count_of_goods = url + '/v3/product/info/stocks'
        data = {
            "filter": {
                "offer_id": [
                    "136834"
                ],
                "product_id": [
                    "214887921"
                ],
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 100
        }

    elif method_of_stock == 'FBS' or method_of_stock == 'rFBS':
        url_to_count_of_goods = url + '/v1/product/info/stocks-by-warehouse/fbs'
        data = {
            "filter": {
                "offer_id": [
                    "136834"
                ],
                "product_id": [
                    "214887921"
                ],
                "visibility": "ALL",
                "sku": [
                    "1234567891"
                ]
            },
            "last_id": "",
            "limit": 100
        }

    else:
        if count_of_stocks == 1:
            url_to_count_of_goods = url + '/v1/product/import/stocks'

        else:
            url_to_count_of_goods = url + '/v2/products/stocks' + identify_of_stock

    return {'url': url_to_count_of_goods, 'data': data}

headers = {
       "Client-Id": client_id,
       "Api-Key": api_key,
       "Content-Type": "application/json"
   }

response = requests.post(count_of_goods(method_of_stock[0], identify_of_stock, count_of_stocks)['url'],
                         headers=headers,
                         json = count_of_goods(method_of_stock[0], identify_of_stock, count_of_stocks)['data'])

if response.status_code == 200:
    data = response.json()
    print(data['result']['total'])

else:
    print(f"Error: {response.status_code}")
    print(response.text)