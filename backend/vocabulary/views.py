from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Word, UserWord
from .serializers import WordSerializer, WordCreateSerializer


class WordViewSet(viewsets.ModelViewSet):
    """单词视图集"""
    queryset = Word.objects.all().order_by('-created_at')
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty']
    search_fields = ['english', 'chinese']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return WordCreateSerializer
        return WordSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        """切换收藏状态"""
        word = self.get_object()
        user_word, _ = UserWord.objects.get_or_create(user=request.user, word=word)
        user_word.is_favorite = not user_word.is_favorite
        user_word.save()
        return Response({'is_favorite': user_word.is_favorite})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_mastered(self, request, pk=None):
        """标记掌握"""
        word = self.get_object()
        user_word, _ = UserWord.objects.get_or_create(user=request.user, word=word)
        user_word.mastered = True
        user_word.save()
        return Response({'mastered': True})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """获取收藏单词"""
        favorite_word_ids = UserWord.objects.filter(
            user=request.user, is_favorite=True
        ).values_list('word_id', flat=True)
        words = Word.objects.filter(id__in=favorite_word_ids)
        page = self.paginate_queryset(words)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unmastered(self, request):
        """获取未掌握单词"""
        mastered_ids = UserWord.objects.filter(
            user=request.user, mastered=True
        ).values_list('word_id', flat=True)
        words = Word.objects.exclude(id__in=mastered_ids)
        page = self.paginate_queryset(words)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def categories(request):
    """获取所有分类"""
    return Response(dict(Word.CATEGORY_CHOICES))
