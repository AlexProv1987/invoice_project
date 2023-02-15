
from django.urls import path
from .views import addproduct, modifyproduct,productdisplay
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('update/<int:pk>/',login_required(modifyproduct.as_view()),name='update-product'),
    path('addproduct/',login_required(addproduct.as_view()),name='add-product'),
    path('viewproducts/',login_required(productdisplay.as_view()),name='view-products'),
]
