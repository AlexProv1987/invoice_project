from django.forms import ModelForm, HiddenInput
from apps.invoice_app.models import invoice
from .models import payment
class paymentform(ModelForm):
    def getinvobj(self):
       print(self.cleaned_data)
    class Meta:
        model = payment
        fields = ('invoice_reltn', 'payment_amt', 'payment_type')
        widgets = {
            'invoice_reltn': HiddenInput,
        }