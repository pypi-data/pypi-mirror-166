from django.urls import path
from product import views

urlpatterns = [
    path('products/', views.GetCreateProductView.as_view(), name = 'get-create-product')
]