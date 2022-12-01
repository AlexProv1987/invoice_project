from django.contrib import admin
from business_app.models import business, client
from product_app.models import product
from invoice_app.models import invoice,invoicefile,lineitem
# Register your models here.

admin.site.register(business)
admin.site.register(client)
admin.site.register(product)
admin.site.register(invoice)
admin.site.register(invoicefile)
admin.site.register(lineitem)