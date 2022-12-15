
from django.views.generic.edit import UpdateView,CreateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from apps.invoice_app.models import invoice
from .models import business,client
from django.utils.decorators import method_decorator
from apps.user_app.models import userassociation
from django.shortcuts import get_object_or_404
#done
class updatebusiness(SuccessMessageMixin,UpdateView):
    model = business
    fields = '__all__'
    template_name='business_form.html'

    def get_success_url(self):
        return reverse('manage-bus')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = f"{self.request.POST['bus_name']} Updated Succesfully"
        if success_message:
            messages.success(self.request, success_message)
        return response

class modifyclient(SuccessMessageMixin,UpdateView):
    model = client
    fields = '__all__'
    template_name='client_form.html'

    def get_success_url(self):
        return reverse('manage-bus')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = success_message = f"{self.request.POST['client_name']} Updated Succesfully"
        if success_message:
            messages.success(self.request, success_message)
        return response

class createclient(SuccessMessageMixin,CreateView):
    model = client
    fields = '__all__'
    template_name='client_form.html'

    def get_success_url(self):
        print(self.request.META.get('HTTP_REFERER'))
        return reverse('manage-bus')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = "Client Created Succesfully"
        if success_message:
            messages.success(self.request, success_message)
        return response     

class invoicedisplay(ListView):
    model = invoice
    fields = '__all__'
    template_name='bus_invs.html'

class invbyclient(TemplateView):
    fields = '__all__'
    template_name='invby_client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        clients = client.objects.all()
        context['business'] = business.business_reltn
        context['clients'] = clients
        print(context)
        return context

class managebusiness(TemplateView):

    template_name= 'business_mngment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        clients = client.objects.all()
        invoices = invoice.objects.filter(bus_reltn=business.business_reltn.pk)
        context['business'] = business.business_reltn
        context['clients'] = clients
        context['invoices'] = invoices
        return context