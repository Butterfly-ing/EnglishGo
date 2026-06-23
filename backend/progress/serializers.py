from rest_framework import serializers
from .models import DailyProgress


class DailyProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = ['id', 'date', 'words_learned', 'words_reviewed',
                  'quiz_count', 'study_minutes', 'checked_in']


class StatsSerializer(serializers.Serializer):
    total_words = serializers.IntegerField()
    learned_words = serializers.IntegerField()
    mastered_words = serializers.IntegerField()
    total_quizzes = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_study_minutes = serializers.IntegerField()
    streak_days = serializers.IntegerField()
