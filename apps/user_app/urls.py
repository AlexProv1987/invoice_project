
from django.urls import path, include
from . import views

urlpatterns = [
    #change this to a landing page
    path('',views.LoginView,name='login-view'),
]
