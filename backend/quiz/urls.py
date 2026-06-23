from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_quiz, name='generate_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('history/<int:pk>/', views.quiz_detail, name='quiz_detail'),
]
