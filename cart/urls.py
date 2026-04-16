from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('add/<str:app_label>/<int:pk>/', views.add_to_cart, name='add'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('delivery-address/', views.delivery_address, name='delivery_address'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('cart-count/', views.get_cart_count, name='cart_count'),
]
