from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表（不含正文）"""
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'title_cn', 'author', 'summary',
            'level', 'tags', 'word_count', 'read_count',
            'created_at', 'updated_at'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    """文章详情（含正文）"""
    class Meta:
        model = Article
        fields = '__all__'
