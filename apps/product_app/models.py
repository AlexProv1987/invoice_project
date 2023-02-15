from django.db import models
from djmoney.models.fields import MoneyField
from apps.business_app.models import business
# Create your models here.
class product(models.Model):
    Available = 1
    OutOfStock = 2
    stock_choices =(
        (1,('Available')),
        (2, ('Out Of Stock')),
    )
    p_name = models.CharField(max_length=50, verbose_name='Product Name', unique=True)
    p_description = models.CharField(max_length=125, verbose_name='Description')
    p_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
        verbose_name='Price'
    )
    p_instock = models.IntegerField(choices=stock_choices, default=Available, verbose_name='Available')
    p_business_reltn = models.ForeignKey(business, on_delete=models.CASCADE, verbose_name='Seller')
    
    def __str__(self):
        return self.p_name
    
    class Meta:
        indexes=[
            models.Index(fields=['p_name',]),
        ]