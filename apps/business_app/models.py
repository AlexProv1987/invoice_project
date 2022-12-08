from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class business(models.Model):
    bus_name = models.CharField(max_length=75)
    bus_street = models.CharField(max_length=50)
    bus_zip = models.IntegerField(blank=False)
    bus_phone = PhoneNumberField(blank=False, unique=True)
    bus_email = models.EmailField(blank=False, unique=True)
    bus_city = models.CharField(max_length=50, default='')
    bus_state = models.CharField(max_length=50, default='')
    def __str__(self):
        return self.bus_name

class client(models.Model):
    client_name = models.CharField(max_length=75)
    client_street = models.CharField(max_length=50)
    client_zip = models.IntegerField(blank=False)
    client_phone = PhoneNumberField(blank=False, unique=True)
    client_email = models.EmailField(blank=False, unique=True)
    client_city = models.CharField(max_length=50, default='')
    client_state = models.CharField(max_length=50, default='')
    def __str__(self):
        return self.client_name