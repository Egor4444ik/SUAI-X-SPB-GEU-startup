# Generated by Django 5.1.2 on 2024-11-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_ozon_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='api_key_ozon',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='user_data',
            name='client_id_ozon',
            field=models.IntegerField(blank=True, default=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_data',
            name='count_of_stocks',
            field=models.IntegerField(blank=True, default=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_data',
            name='identify_of_stock',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]