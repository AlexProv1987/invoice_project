from tkinter import CASCADE
from django.db import models
from business_app.models import business,client
from product_app.models import product
from djmoney.models.fields import MoneyField
# Create your models here.
'''
I am choosing not to cascade anything here for fkey's on delete as a safety precaution for unintentional data loss
'''
class invoice(models.Model):
    inv_status_choices = (
        (1,'Billed'),
        (2,'Paid'),
    )
    bus_reltn = models.ForeignKey(business, on_delete=models.PROTECT)
    client_reltn = models.ForeignKey(client,on_delete=models.PROTECT)
    line_item_cnt = models.IntegerField(blank=False)
    product_qty = models.IntegerField(blank=False)
    total_billed = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    inv_status = models.IntegerField(choices=inv_status_choices)
    inv_billed_date = models.DateField()
    inv_paid_date = models.DateField(null=True)

class invoicefile(models.Model):
    inv_reltn = models.ForeignKey(invoice,on_delete=models.PROTECT)
    file_loc = models.CharField(max_length=150, blank=False)

class lineitem(models.Model):
    inv_reltn = models.ForeignKey(invoice,on_delete=models.PROTECT)
    product = models.ForeignKey(product,on_delete=models.PROTECT)
    line_item_qty = models.IntegerField()
    line_item_amt = models.IntegerField()
