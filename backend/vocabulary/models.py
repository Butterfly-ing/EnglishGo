from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    """单词表"""
    CATEGORY_CHOICES = [
        ('basic', '基础'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
        ('business', '商务'),
        ('travel', '旅游'),
        ('junior', '初中'),
        ('senior', '高中'),
        ('cet4', '四级'),
        ('cet6', '六级'),
        ('postgraduate', '考研'),
        ('toefl', '托福'),
        ('sat', 'SAT'),
    ]
    PART_OF_SPEECH_CHOICES = [
        ('noun', '名词'),
        ('verb', '动词'),
        ('adjective', '形容词'),
        ('adverb', '副词'),
        ('preposition', '介词'),
        ('conjunction', '连词'),
        ('pronoun', '代词'),
        ('phrase', '短语'),
    ]

    english = models.CharField(max_length=200, verbose_name='英文')
    chinese = models.CharField(max_length=200, verbose_name='中文释义')
    phonetic = models.CharField(max_length=200, blank=True, default='', verbose_name='音标')
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH_CHOICES, default='noun', verbose_name='词性')
    example = models.TextField(blank=True, default='', verbose_name='例句')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='basic', verbose_name='分类')
    difficulty = models.IntegerField(default=1, verbose_name='难度(1-5)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'word'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['difficulty']),
        ]

    def __str__(self):
        return f'{self.english} - {self.chinese}'


class UserWord(models.Model):
    """用户-单词关系表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='user_words')
    is_favorite = models.BooleanField(default=False, verbose_name='是否收藏')
    mastered = models.BooleanField(default=False, verbose_name='是否掌握')
    practice_count = models.IntegerField(default=0, verbose_name='练习次数')
    correct_count = models.IntegerField(default=0, verbose_name='正确次数')
    last_practiced = models.DateTimeField(null=True, blank=True, verbose_name='最后练习时间')

    class Meta:
        db_table = 'user_word'
        unique_together = ['user', 'word']

    def __str__(self):
        return f'{self.user.username} - {self.word.english}'
