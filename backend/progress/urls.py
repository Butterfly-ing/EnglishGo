from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_stats, name='stats'),
    path('daily/', views.get_daily, name='daily'),
    path('checkin/', views.checkin, name='checkin'),
    path('record_activity/', views.record_activity, name='record_activity'),
]
