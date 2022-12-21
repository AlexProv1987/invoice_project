from django_filters import FilterSet
import django_filters as filters
from .models import client
from apps.invoice_app.models import invoice
class clientfilter(FilterSet):
    client_name = filters.CharFilter(field_name='client_name', lookup_expr='icontains', label='Client Name: ')
    class Meta:
        model = client
        fields = []

class invoicefilter(FilterSet):
    invoice_status = filters.ChoiceFilter(field_name='inv_status',lookup_expr='icontains', choices=invoice.inv_status_choices,empty_label='----------',label='Status')
    invoice_nbr = filters.NumberFilter(field_name='id', lookup_expr='exact', label='Invoice#')
    invoice_client = filters.ModelChoiceFilter(field_name='client_reltn', queryset=client.objects.all(), label='Client')
    invoice_remaining_amt = filters.NumberFilter(field_name='curr_amt_due',lookup_expr='gte', label='Amount Due: ')
    class Meta:
        model = invoice
        fields=[]