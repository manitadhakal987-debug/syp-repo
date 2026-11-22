from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('haircut-guide/', views.haircut_guide_list_view, name='haircut_guides'),
    path('haircut-guide/<slug:slug>/', views.haircut_guide_detail_view, name='haircut_guide_detail'),
]
