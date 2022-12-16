from django.views.generic.edit import UpdateView,CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import payment
from django.contrib import messages
from django.urls import reverse
from .controllers.postpayment import postpayment
from  . import modelforms
from django.http import HttpResponse
class makepayment(SuccessMessageMixin,CreateView):
    model = payment
    template_name = 'payment_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('manage-bus')

    def form_valid(self, form):
        print(self.request.POST)
        response = super().form_valid(form)
        postpayment(self.request.POST)
        success_message = f"asdfasdfsdf"
        if success_message:
            messages.success(self.request, success_message)
        return response