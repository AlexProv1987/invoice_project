from django.db import models
from djmoney.models.fields import MoneyField
from apps.business_app.models import business
# Create your models here.
class product(models.Model):
    p_name = models.CharField(max_length=50)
    p_description = models.CharField(max_length=125)
    p_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    p_is_active = models.BooleanField(default=True)
    p_business_reltn = models.ForeignKey(business, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.p_name