from django.urls import path
from . import views

urlpatterns = [
    path('add_customers', views.add_customers),
    path('get_customers/<int:user_id>', views.get_customers),
    path('update_customers/<int:id>', views.update_customers),
    path('filter_customers', views.filter_customers)
]