from django.contrib import admin
from apps.business_app.models import business, client
from apps.product_app.models import product
from apps.invoice_app.models import invoice,lineitem
from apps.user_app.models import userassociation
from apps.payment_app.models import payment
# Register your models here.
@admin.register(userassociation)
class userassocadmin(admin.ModelAdmin):
    list_display = ('user_reltn', 'business_reltn')

@admin.register(product)
class productadmin(admin.ModelAdmin):
    list_display = ('p_name', 'p_business_reltn')

@admin.register(invoice)
class invoiceadmin(admin.ModelAdmin):
    list_display = ('id', 'bus_reltn')

admin.site.register(business)
admin.site.register(client)
admin.site.register(lineitem)
admin.site.register(payment)