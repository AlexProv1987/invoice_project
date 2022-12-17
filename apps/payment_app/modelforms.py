from django.forms import ModelForm
from apps.invoice_app.models import invoice
from .models import payment

class paymentform(ModelForm):

    def __init__(self, pk,*args, **kwargs):      
        super(paymentform, self).__init__(*args, **kwargs)
        self.fields['invoice_reltn'].choices = invoice.objects.filter(pk=pk)
        self.fields['invoice_reltn'].initial = self.fields['invoice_reltn'].choices[0] 

    class Meta:
        model = payment
        fields ='__all__'