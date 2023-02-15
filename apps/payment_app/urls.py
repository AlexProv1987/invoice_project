
from django.urls import path
from .views import makepayment
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('payment/<int:pk>',login_required(makepayment.as_view()), name='make-payment'),
]
