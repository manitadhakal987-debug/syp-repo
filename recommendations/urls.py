from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('routine/', views.routine_detail_view, name='routine_detail'),
    path('compatibility/', views.compatibility_checker_view, name='compatibility_checker'),
]
