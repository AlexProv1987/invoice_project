
from django.urls import path
from .views import makepayment
urlpatterns = [
    path('payments/<int:pk>',makepayment.as_view(), name='make-payment'),
]
