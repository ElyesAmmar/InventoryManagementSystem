from django.urls import path
from . import views

urlpatterns = [
    path('add_product', views.add_products),
    path('get_product', views.get_products),
    path('update_product/<int:id>', views.update_product),
    path('filter_products', views.filter_products)
]