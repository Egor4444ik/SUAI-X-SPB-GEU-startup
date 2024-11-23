from django.conf import settings
from django.db import models
from .API_ozon import take_fullfilment, count_of_goods

class user_data(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=False, null=True)
    age = models.IntegerField(blank=False)
    region = models.CharField(blank=False, max_length=20)
    sex = models.CharField(blank=False, max_length=1)
    api_key_ozon = models.CharField(blank=True, max_length=36)
    client_id_ozon = models.CharField(blank=True, max_length=20)
    identify_of_stock = models.CharField(blank=True, max_length=20)
    count_of_stocks = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return f'Profile of {self.user.username}'


class ozon(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    def update_data(self):
        ozon_goods_cards = ['iphone_16', 'iphone_16_pro_max']
        all_data = {}

        for goods_card in ozon_goods_cards:
            try:
                attrs = self.get_ozon_data(goods_card)
                if attrs:
                  all_data[goods_card] = attrs
            except Exception as e:
                print(f"Ошибка при получении данных для {goods_card}: {e}")

        self.data = all_data
        self.save()
        print('data has been updated')

    def get_ozon_data(self, goods_card):
        user_data_instance = getattr(self.user, 'user_data', None)
        if not user_data_instance:
            print("user_data not found for this user")
            return None

        try:
            #Обработка ошибок 403 непосредственно внутри take_fullfilment, если это возможно.
            client_id=user_data_instance.client_id_ozon
            api_key=user_data_instance.api_key_ozon
            fbs_data = take_fullfilment(Client_Id=client_id, Api_key=api_key, Stock_method='FBS', offer_id=offer_id, product_id=product_id)
            fbo_data = take_fullfilment(Client_Id=client_id, Api_key=api_key, Stock_method='FBO', offer_id=offer_id, product_id=product_id)
            other_fullfilment_data = take_fullfilment(Client_Id=client_id, Api_key=api_key, count_of_stocks=user_data_instance.count_of_stocks,
                                          identify_of_stock=user_data_instance.identify_of_stock, offer_id=offer_id, product_id=product_id)
            attrs = {
              'category': 'Phone',
              'offer_id': '123456',
              'product_id': '123456',
              'count_from_FBS': str(fbs_data),
              'count_from_FBO': str(fbo_data),
              'count_from_other_fullfilment': str(other_fullfilment_data),
              'buyer_name': 'Some Buyer',
              'buyer_sex': 'Male',
              'buyer_age': '30',
              'buyer_region': 'Moscow',
              'buyer_num_session': '5',
              'buyer_avg_session': '15',
              'date': '2024-10-27',
            }
            return attrs
        except Exception as e:
            print(f"Ошибка API Ozon: {e}")
            return None

    def __str__(self):
      return f'OZON analitic of {self.user.username}'