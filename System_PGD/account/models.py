from django.db import models
from django.conf import settings

class user_data(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True, max_length=2)
    region = models.CharField(blank=True, null=True)
    sex = models.CharField(blank=True, null=True, max_length=1)

    class user_cards(models.Model):
        category = models.CharField(blank=True, null=True)
        card_name = models.CharField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'