from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list(request):
    """文章列表（分页 + 筛选）"""
    queryset = Article.objects.all()

    # 按难度筛选
    level = request.query_params.get('level', '')
    if level:
        queryset = queryset.filter(level=level)

    # 搜索（标题和摘要）
    search = request.query_params.get('search', '')
    if search:
        queryset = queryset.filter(title__icontains=search) | queryset.filter(summary__icontains=search)

    # 分页
    paginator = ArticlePagination()
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = ArticleListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = ArticleListSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, pk):
    """文章详情（阅读计数 +1）"""
    article = get_object_or_404(Article, pk=pk)
    Article.objects.filter(pk=pk).update(read_count=F('read_count') + 1)
    article.refresh_from_db()
    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_levels(request):
    """获取难度分类"""
    return Response(dict(Article.LEVEL_CHOICES))
