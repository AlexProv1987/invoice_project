from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from .models import product
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
#when updating or adding well redirect back to product list with a message using message framework
class addproduct(SuccessMessageMixin,CreateView):
    model = product
    fields = '__all__'
    template_name='add_product.html'
    sucess_message = 'Product Created Succesfully'

    def get_success_url(self):
        return reverse('view-products')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = f"{self.request.POST['p_name']} Created Succesfully"
        if success_message:
            messages.success(self.request, success_message)
        return response

class modifyproduct(SuccessMessageMixin,UpdateView):
    model = product
    fields = '__all__'
    template_name='update_product.html'

    def get_success_url(self):
        return reverse('view-products')

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = f"Product {self.request.POST['p_name']} Updated"
        if success_message:
            messages.success(self.request, success_message)
        return response
        
class productdisplay(ListView):
    model = product
    fields = '__all__'
    template_name='product_list.html'
    def get_success_url(self):
        return reverse('view-products')