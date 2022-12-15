from django.urls import path
from . import views
urlpatterns = [
    path('invgen/', views.invoicegen, name='invoice-gen' ),
    path('invview/<str:bus>/<int:pk>', views.invoicesview, name='inv-view'),
    path('pdfdownload/<str:bus>/<int:pk>', views.downloadpdf, name='download-pdf'),
    path('modifyinv/<str:bus>/<int:pk>', views.updateinvoicestatus,name='modify-inv'),
    path('cancelinv/<str:bus>/<int:pk>', views.cancelinvoice, name='cancel-inv')
]