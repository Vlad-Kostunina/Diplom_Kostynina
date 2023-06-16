from django.db import models

# Create your models here.
class Indicator(models.Model):
    pression=models.FloatField('Давление')
    temperature=models.FloatField('Температура')
    humidity=models.FloatField('Влажность')
