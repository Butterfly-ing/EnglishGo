from rest_framework import serializers
from .models import QuizRecord, QuizDetail


class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizDetail
        fields = ['id', 'word_id', 'question', 'correct_answer', 'user_answer', 'is_correct']


class QuizRecordSerializer(serializers.ModelSerializer):
    details = QuizDetailSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = QuizRecord
        fields = ['id', 'username', 'quiz_type', 'total_questions',
                  'correct_answers', 'score', 'completed_at', 'details']


class QuizRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRecord
        fields = ['id', 'quiz_type', 'total_questions', 'correct_answers',
                  'score', 'completed_at']


class GenerateQuizSerializer(serializers.Serializer):
    quiz_type = serializers.ChoiceField(choices=['choice', 'spelling', 'listening'])
    question_count = serializers.IntegerField(default=10, min_value=1, max_value=50)
    category = serializers.CharField(required=False, allow_blank=True, default='')
    difficulty = serializers.IntegerField(required=False, allow_null=True, default=None)


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField(allow_blank=True)
