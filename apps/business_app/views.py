
from django.views.generic.edit import UpdateView,CreateView
from django_filters.views import FilterView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from apps.invoice_app.models import invoice
from .models import business,client
from .businessapp_filters import clientfilter, invoicefilter
from apps.user_app.models import userassociation
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
        return reverse('view-clients')

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

class invoicedisplay(FilterView):
    queryset=invoice.objects.all()
    template_name='bus_invs.html'
    filterset_class=invoicefilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        context['business'] = business.business_reltn
        return context

class invbyclient(FilterView):
    template_name='invby_client.html'
    filterset_class=invoicefilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        clients = client.objects.get(pk=self.kwargs['pk'])
        self.queryset = invoice.objects.filter(client_reltn=clients)
        context['business'] = business.business_reltn
        context['clients'] = clients
        return context

class managebusiness(TemplateView):
    template_name= 'business_mngment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        context['business'] = business.business_reltn
        return context

class viewclients(FilterView):
    queryset=client.objects.all()
    template_name = 'view_clients.html'
    filterset_class=clientfilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = userassociation.objects.get(user_reltn=self.request.user.pk)
        context['business'] = business.business_reltn
        return context