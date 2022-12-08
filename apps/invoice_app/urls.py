from django.urls import path
from . import views
urlpatterns = [
    path('invgen/', views.invoicegen, name='invoice-gen' ),
]