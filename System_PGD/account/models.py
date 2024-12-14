from django.conf import settings
from django.db import models
from .API_ozon import take_info, goods_info
import time

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
        current_data = self.data.copy()

        for goods_card in ozon_goods_cards:
            try:
                attrs = self.get_ozon_data(goods_card, current_data)
                if attrs:
                    self.data[goods_card] = attrs  # Обновляем только необходимый goods_card
            except Exception as e:
                print(f"Ошибка при получении данных для {goods_card}: {e}")

        self.save()
        print('data has been updated')

    def get_ozon_data(self, goods_card, old_data):
        user_data_instance = getattr(self.user, 'user_data', None)
        if not user_data_instance:
            print("user_data not found for this user")
            return None

        try:
            client_id = user_data_instance.client_id_ozon
            api_key = user_data_instance.api_key_ozon

            take_fbs_data = take_info(Client_Id=client_id, Api_key=api_key, Stock_method='FBS', offer_id='123456', product_id='123456')
            o_d_fbs = old_data[goods_card]['count_from_FBS'] if old_data else []
            fbs_data = ([o_d_fbs] if type(o_d_fbs) != list else o_d_fbs)+[take_fbs_data]

            take_fbo_data = take_info(Client_Id=client_id, Api_key=api_key, Stock_method='FBO', offer_id='123456', product_id='123456')
            o_d_fbo = old_data[goods_card]['count_from_FBO'] if old_data else []
            fbo_data = ([o_d_fbo] if type(o_d_fbo) != list else o_d_fbo) + [take_fbo_data['items'] if take_fbo_data['items'] != [] else None]

            if user_data_instance.identify_of_stock != "":
                take_other_fullfilment_data = take_info(Client_Id=client_id, Api_key=api_key, count_of_stocks=int(user_data_instance.count_of_stocks),
                                                   identify_of_stock=int(user_data_instance.identify_of_stock), offer_id='123456', product_id='123456')
            else: take_other_fullfilment_data = None
            o_d_tof = old_data[goods_card]['count_from_other_fullfilment'] if old_data else []
            other_fullfilment_data = ([o_d_tof] if type(o_d_tof) != list else o_d_tof) + [take_other_fullfilment_data]

            o_d_date = old_data[goods_card]['date'] if old_data else []
            date = ([o_d_date] if type(o_d_date) != list else o_d_date) + [time.strftime("%Y-%m-%d")]

            take_price = take_info(Client_Id=client_id, Api_key=api_key, take_price='True', offer_id='123456', product_id='123456')
            o_d_price = old_data[goods_card]['price'] if old_data else []
            price = ([o_d_price] if type(o_d_price) != list else o_d_price) + [take_price]

            take_buyer_name = 'Some Buyer'
            o_d_buyer_name = old_data[goods_card]['buyer_name'] if old_data else []
            buyer_name = ([o_d_buyer_name] if type(o_d_buyer_name) != list else o_d_buyer_name) + [take_buyer_name]

            take_buyer_sex = 'Some sex'
            o_d_buyer_sex = old_data[goods_card]['buyer_sex'] if old_data else []
            buyer_sex = ([o_d_buyer_sex] if type(o_d_buyer_sex) != list else o_d_buyer_sex) + [take_buyer_sex]

            take_buyer_age = 'Some age'
            o_d_buyer_age = old_data[goods_card]['buyer_age'] if old_data else []
            buyer_age = ([o_d_buyer_age] if type(o_d_buyer_age) != list else o_d_buyer_age) + [take_buyer_age]

            take_buyer_region = 'Some region'
            o_d_buyer_region = old_data[goods_card]['buyer_region'] if old_data else []
            buyer_region = ([o_d_buyer_region] if type(o_d_buyer_region) != list else o_d_buyer_region) + [take_buyer_region]

            take_buyer_num_session = 'Some digit'
            o_d_buyer_num_session = old_data[goods_card]['buyer_num_session'] if old_data else []
            buyer_num_session = ([o_d_buyer_num_session] if type(o_d_buyer_num_session) != list else o_d_buyer_num_session) + [take_buyer_num_session]

            # Правильная обработка данных из API.  Проверьте структуру данных, возвращаемых take_info
            attrs = {
                'category': 'Tech',
                'undercategory': 'Iphone',
                'underundercategory': 'Iphone_new_gen',
                'offer_id': '123456',
                'product_id': '123456',
                'count_from_FBS': fbs_data if fbs_data else [],
                'count_from_FBO': fbo_data if fbo_data else [],
                'count_from_other_fullfilment': other_fullfilment_data if other_fullfilment_data else [],
                'buyer_name': buyer_name if buyer_name else [],
                'buyer_sex': buyer_sex if buyer_sex else [],
                'buyer_age': buyer_age if buyer_age else [],
                'buyer_region': buyer_region if buyer_region else [],
                'buyer_num_session': buyer_num_session if buyer_num_session else [],
                'date': date,
                'price': price
            }

            return attrs
        except Exception as e:
            print(f"Ошибка API Ozon: {e}")
            return None

    def __str__(self):
      return f'OZON analitic of {self.user.username}'