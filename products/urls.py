from django.urls import path
from . import views

urlpatterns = [
    path('add_product', views.add_products),
    path('get_product', views.get_products),
]