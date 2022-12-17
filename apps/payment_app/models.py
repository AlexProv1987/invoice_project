from django.db import models
from djmoney.models.fields import MoneyField
from apps.invoice_app.models import invoice

class payment(models.Model):
    Debit = 1
    Credit = 2
    payment_type_choices = (
        (Debit,('Debit')),
        (Credit,('Credit'))    
    )
    invoice_reltn = models.ForeignKey(invoice,on_delete=models.PROTECT)
    payment_amt = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
        verbose_name='Amount'
    )
    payment_type = models.IntegerField(choices=payment_type_choices, verbose_name='Type')
    posted_date = models.DateField(auto_now_add=True)
