from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('result/<int:profile_id>/', views.quiz_result_view, name='result'),
    path('retake/', views.retake_quiz_view, name='retake'),
]
