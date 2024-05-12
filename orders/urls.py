from django.urls import path
from . import views

urlpatterns = [
    path('create_orders/<int:user_id>', views.create_order),
    path('update_orders/<int:id>', views.update_order),
    path('get_orders/<int:user_id>', views.get_orders),
    path('get_order/<int:id>', views.get_order_details),
    path('generate_invoice/<int:id>', views.generate_invoice)
]