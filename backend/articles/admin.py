from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'level', 'word_count', 'read_count', 'created_at']
    list_filter = ['level']
    search_fields = ['title', 'summary']
