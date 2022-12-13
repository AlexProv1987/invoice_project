from django.db import models
from apps.business_app.models import business,client
from apps.product_app.models import product
from django.urls import reverse
from djmoney.models.fields import MoneyField
from django.utils.text import slugify
# Create your models here.
'''
I am choosing not to cascade anything here for fkey's on delete as a safety precaution for unintentional data loss
'''
class invoice(models.Model):
    Generated = 1
    Billed = 2
    Paid = 3
    ReadyToBill = 4
    Cancelled = 5
    inv_status_choices = (
        (Generated,('Generated')),
        (Billed,('Billed')),
        (Paid,('Paid')),
        (ReadyToBill,('Ready To Bill')),
        (Cancelled,('Cancelled')),
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
    inv_billed_date = models.DateField(null=True)
    inv_paid_date = models.DateField(null=True)
    inv_generated_date=models.DateTimeField(null=True)
class invoicefile(models.Model):
    inv_reltn = models.ForeignKey(invoice,on_delete=models.PROTECT)
    inv_slug = models.SlugField(editable=False,null=False, max_length=275, unique=True, default='')
    file_loc = models.CharField(max_length=150, blank=False)
    '''Slug field is currently unused here, leaving impleneted for now in case we decide to use it for url gen'''
    def get_absolute_url(self):
        kwargs = {'pk': self.inv_reltn.pk,'slug': self.inv_reltn.bus_reltn.bus_name
        }
        return reverse('inv-submit', kwargs=kwargs)

    def save(self,*args,**kwargs):
        value = self.inv_reltn.pk
        self.inv_slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
class lineitem(models.Model):
    inv_reltn = models.ForeignKey(invoice,on_delete=models.PROTECT)
    product = models.ForeignKey(product,on_delete=models.PROTECT, blank=False)
    line_item_qty = models.PositiveBigIntegerField(blank=False)
    line_item_amt = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
