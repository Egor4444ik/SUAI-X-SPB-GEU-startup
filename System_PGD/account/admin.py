from django.contrib import admin
from .models import ozon, user_data
@admin.register(user_data)
class User_DataAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'age', 'region', 'sex', 'api_key_ozon', 'client_id_ozon', 'identify_of_stock', 'count_of_stocks']
    raw_id_fields = ['user']

@admin.register(ozon)
class User_OzonAdmin(admin.ModelAdmin):
    list_display = ['user', 'data'] #+ozon.app_labels
    raw_id_fields = ['user']