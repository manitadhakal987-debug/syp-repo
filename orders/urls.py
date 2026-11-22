from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/', views.update_cart_view, name='update_cart'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('history/', views.order_history_view, name='order_history'),
    path('esewa/initiate/<str:order_number>/', views.esewa_initiate_view, name='esewa_initiate'),
    path('esewa/success/', views.esewa_success_view, name='esewa_success'),
    path('esewa/failure/', views.esewa_failure_view, name='esewa_failure'),
]
