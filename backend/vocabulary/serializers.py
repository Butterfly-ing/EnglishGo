from rest_framework import serializers
from .models import Word, UserWord


class WordSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    mastered = serializers.SerializerMethodField()
    practice_count = serializers.SerializerMethodField()
    correct_count = serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = [
            'id', 'english', 'chinese', 'phonetic', 'part_of_speech',
            'example', 'category', 'difficulty', 'created_at',
            'is_favorite', 'mastered', 'practice_count', 'correct_count'
        ]

    def _get_user_word(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserWord.objects.filter(user=request.user, word=obj).first()
        return None

    def get_is_favorite(self, obj):
        uw = self._get_user_word(obj)
        return uw.is_favorite if uw else False

    def get_mastered(self, obj):
        uw = self._get_user_word(obj)
        return uw.mastered if uw else False

    def get_practice_count(self, obj):
        uw = self._get_user_word(obj)
        return uw.practice_count if uw else 0

    def get_correct_count(self, obj):
        uw = self._get_user_word(obj)
        return uw.correct_count if uw else 0


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['english', 'chinese', 'phonetic', 'part_of_speech', 'example', 'category', 'difficulty']
