from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.models import USStateField
class business(models.Model):
    bus_name = models.CharField(max_length=75, verbose_name='Business Name')
    bus_street = models.CharField(max_length=50, verbose_name='Street')
    bus_zip = models.IntegerField(blank=False,verbose_name='Zip')
    bus_phone = PhoneNumberField(blank=False, unique=True, verbose_name='Phone')
    bus_email = models.EmailField(blank=False, unique=True, verbose_name='Email')
    bus_city = models.CharField(max_length=50, default='', verbose_name='City')
    bus_state = USStateField()
    #add business logo path here
    def __str__(self):
        return self.bus_name

class client(models.Model):
    client_name = models.CharField(max_length=75, unique=True)
    client_street = models.CharField(max_length=50)
    client_zip = models.IntegerField(blank=False)
    client_phone = PhoneNumberField(blank=True, unique=True)
    client_email = models.EmailField(blank=False, unique=True)
    client_city = models.CharField(max_length=50, default='')
    client_state = USStateField()
    def __str__(self):
        return self.client_name

