from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import payment
from django.contrib import messages
from django.urls import reverse
from .controllers.postpayment import postpayment
from  .modelforms import paymentform

class makepayment(SuccessMessageMixin,CreateView):
    model = payment
    template_name = 'payment_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(makepayment,self).get_context_data(**kwargs)
        form = paymentform(pk=self.kwargs['pk'])
        context['form'] = form
        #context['form'].fields['invoice_reltn'].initial = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('view-invoices')

    def form_valid(self, form):
        #we need to understand form_valid more grab the object it creates in case we fail applying it to the invoice curr amt due
        response = super().form_valid(form)
        postpmt = postpayment(self.request.POST)
        if postpmt._postpayment():
            success_message = f"Payment Of ${self.request.POST['payment_amt_0']} Applied to INV#{self.request.POST['invoice_reltn']}"
            if success_message:
                messages.success(self.request, success_message)
            return response
        else: 
            messages.error(self.request,postpmt.return_message)
            return response
            
