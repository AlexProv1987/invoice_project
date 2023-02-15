
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import viewclients,updatebusiness,modifyclient, createclient, invoicedisplay,managebusiness, invbyclient
urlpatterns = [
    path('managebus/',login_required(managebusiness.as_view()), name='manage-bus'),
    path('updatebusiness/<int:pk>/',login_required(updatebusiness.as_view()),name='update-business'),
    path('updateclient/<int:pk>',login_required(modifyclient.as_view()),name='update-client'),
    path('createclient/',login_required(createclient.as_view()),name='create-client'),
    path('businvoices/',login_required(invoicedisplay.as_view()),name='view-invoices'),
    path('invbyclient/<int:pk>',login_required(invbyclient.as_view()), name='inv-byclient'),
    path('clientlist/', login_required(viewclients.as_view()), name='view-clients')
]
