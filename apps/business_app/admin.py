from django.contrib import admin
from apps.business_app.models import business, client
from apps.product_app.models import product
from apps.invoice_app.models import invoice,invoicefile,lineitem
# Register your models here.

admin.site.register(business)
admin.site.register(client)
admin.site.register(product)
admin.site.register(invoice)
admin.site.register(invoicefile)
admin.site.register(lineitem)