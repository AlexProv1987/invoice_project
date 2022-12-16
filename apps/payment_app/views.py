from django.views.generic.edit import UpdateView,CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import payment
from django.contrib import messages
from django.urls import reverse
from .controllers.postpayment import postpayment
class makepayment(SuccessMessageMixin,CreateView):
    model = payment
    fields = '__all__'
    template_name = 'payment_form.html'

    def get_success_url(self):
        return reverse('manage-bus')

    def form_valid(self, form):
        response = super().form_valid(form)
        print(self.request.POST)
        postpayment()
        success_message = f"ddddddd"
        if success_message:
            messages.success(self.request, success_message)
        return response