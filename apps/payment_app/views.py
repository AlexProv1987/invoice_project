from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import payment
from django.contrib import messages
from django.urls import reverse
from .controllers.postpayment import postpayment
from  .modelforms import paymentform
from django.http import HttpResponseRedirect
class makepayment(SuccessMessageMixin,CreateView):
    model = payment
    template_name = 'payment_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(makepayment,self).get_context_data(**kwargs)
        form = paymentform(pk=self.kwargs['pk'])
        context['form'] = form
        context['inv'] = self.kwargs['pk']
        #context['form'].fields['invoice_reltn'].initial = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('view-invoices')

    #postpayment class will be our validator to return a response, we cannot use the default as even if we catch errors well save as its a part of the default form_valid method.
    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            postpmt = postpayment(self.request.POST)  
            if postpmt._postpayment():
                form.save()
                success_message = f"Payment Of ${self.request.POST['payment_amt_0']} Applied to INV#{self.request.POST['invoice_reltn']}"
                if success_message:
                    messages.success(self.request, success_message)
                return HttpResponseRedirect (self.get_success_url())
            else: 
                messages.error(self.request,postpmt.return_message)
                return HttpResponseRedirect (self.request.META.get('HTTP_REFERER'))
            
