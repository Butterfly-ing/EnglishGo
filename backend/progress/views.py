from datetime import date, timedelta
from django.db import models
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vocabulary.models import Word, UserWord
from quiz.models import QuizRecord
from .models import DailyProgress
from .serializers import DailyProgressSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    """获取学习统计"""
    user = request.user

    total_words = Word.objects.count()
    learned_words = UserWord.objects.filter(user=user, practice_count__gt=0).count()
    mastered_words = UserWord.objects.filter(user=user, mastered=True).count()

    quiz_records = QuizRecord.objects.filter(user=user)
    total_quizzes = quiz_records.count()
    avg_score = quiz_records.aggregate(models.Avg('score'))['score__avg'] or 0

    total_minutes = DailyProgress.objects.filter(user=user).aggregate(
        models.Sum('study_minutes')
    )['study_minutes__sum'] or 0

    # 计算连续打卡天数
    streak = _calculate_streak(user)

    return Response({
        'total_words': total_words,
        'learned_words': learned_words,
        'mastered_words': mastered_words,
        'total_quizzes': total_quizzes,
        'average_score': round(avg_score, 1),
        'total_study_minutes': total_minutes,
        'streak_days': streak
    })


def _calculate_streak(user):
    """计算连续打卡天数"""
    today = timezone.localdate()
    streak = 0
    for i in range(365):
        check_date = today - timedelta(days=i)
        progress = DailyProgress.objects.filter(
            user=user, date=check_date, checked_in=True
        ).first()
        if progress:
            streak += 1
        elif i == 0:
            continue  # 今天可能还没打卡
        else:
            break
    return streak


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily(request):
    """获取每日进度"""
    days = int(request.query_params.get('days', 30))
    today = timezone.localdate()
    start_date = today - timedelta(days=days - 1)

    progress = DailyProgress.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today
    ).order_by('date')

    serializer = DailyProgressSerializer(progress, many=True)
    return Response({'results': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkin(request):
    """今日打卡"""
    today = timezone.localdate()
    progress, created = DailyProgress.objects.get_or_create(
        user=request.user, date=today,
        defaults={'words_learned': 0, 'words_reviewed': 0,
                  'quiz_count': 0, 'study_minutes': 0}
    )

    if not progress.checked_in:
        progress.checked_in = True
        progress.save()

    # 统计今日数据
    today_word_count = UserWord.objects.filter(
        user=request.user, last_practiced__date=today
    ).count()

    streak = _calculate_streak(request.user)

    return Response({
        'checked_in': True,
        'streak_days': streak,
        'today_words': today_word_count,
        'today_minutes': progress.study_minutes
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_activity(request):
    """记录学习活动"""
    today = timezone.localdate()
    progress, _ = DailyProgress.objects.get_or_create(
        user=request.user, date=today,
        defaults={'words_learned': 0, 'words_reviewed': 0,
                  'quiz_count': 0, 'study_minutes': 0}
    )

    words_learned = request.data.get('words_learned', 0)
    words_reviewed = request.data.get('words_reviewed', 0)
    study_minutes = request.data.get('study_minutes', 0)

    progress.words_learned += words_learned
    progress.words_reviewed += words_reviewed
    progress.study_minutes += study_minutes

    if not progress.checked_in and (words_learned > 0 or words_reviewed > 0):
        progress.checked_in = True

    progress.save()

    return Response(DailyProgressSerializer(progress).data)
