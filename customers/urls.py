from django.urls import path
from . import views

urlpatterns = [
    path('add_customers', views.add_customers)
]