
from django.urls import path
from .views import updatebusiness,modifyclient, createclient, invoicedisplay,managebusiness, invbyclient
urlpatterns = [
    path('managebus/',managebusiness.as_view(), name='manage-bus'),
    path('updatebusiness/<int:pk>/',updatebusiness.as_view(),name='update-business'),
    path('updateclient/<int:pk>',modifyclient.as_view(),name='update-client'),
    path('createclient/',createclient.as_view(),name='create-client'),
    path('businvoices/',invoicedisplay.as_view(),name='view-invoices'),
    path('invbyclient/<int:pk>',invbyclient.as_view(), name='inv-byclient' )
]
