from django.forms import ModelForm,modelformset_factory
from django import forms
from .models import invoice, lineitem

'''option widget selectors'''
class businessselect(forms.Select):
     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['bus-name'] = value.instance.bus_name
        return option

class clientselect(forms.Select):
     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['client-name'] = value.instance.client_name
        return option

class productselect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['product'] = value.instance.p_name
        return option

'''model form classes'''
class invoiceform(ModelForm):
    class Meta:
        model = invoice
        fields = ['bus_reltn', 'client_reltn']
        labels = {
            'bus_reltn': 'Billed From',
            'client_reltn': 'Billed To'
        }
        widgets = {
            'bus_options': businessselect,
            'client_options': clientselect
        }


class lineitemform(ModelForm):
    class Meta:
        model = lineitem
        fields = ['product', 'line_item_qty']
        labels = {
            'product': 'Product',
            'line_item_qty': 'Units'
        }
        widgets = {
            'product_options': productselect
        }

lineitemformset = modelformset_factory(
    lineitem, fields=("product", "line_item_qty"),labels={'product': 'Product','line_item_qty': 'Units'}, extra=1
)