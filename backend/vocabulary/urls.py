from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'words', views.WordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.categories, name='categories'),
]
