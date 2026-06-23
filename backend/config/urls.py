from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/vocabulary/', include('vocabulary.urls')),
    path('api/v1/quiz/', include('quiz.urls')),
    path('api/v1/progress/', include('progress.urls')),
    path('api/v1/articles/', include('articles.urls')),
]
