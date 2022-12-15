
from django.urls import path
from .views import addproduct, modifyproduct,productdisplay
urlpatterns = [
    path('update/<int:pk>/',modifyproduct.as_view(),name='update-product'),
    path('addproduct/',addproduct.as_view(),name='add-product'),
    path('viewproducts/',productdisplay.as_view(),name='view-products'),
]
