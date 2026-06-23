from django.db import models
from django.contrib.auth.models import User


class QuizRecord(models.Model):
    """测验记录"""
    QUIZ_TYPE_CHOICES = [
        ('choice', '选择题'),
        ('spelling', '拼写题'),
        ('listening', '英译中'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_records')
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, verbose_name='测验类型')
    total_questions = models.IntegerField(default=0, verbose_name='总题数')
    correct_answers = models.IntegerField(default=0, verbose_name='正确数')
    score = models.FloatField(default=0, verbose_name='得分')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='完成时间')

    class Meta:
        db_table = 'quiz_record'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user.username} - {self.quiz_type} - {self.score}%'


class QuizDetail(models.Model):
    """测验详情"""
    quiz_record = models.ForeignKey(QuizRecord, on_delete=models.CASCADE, related_name='details')
    word_id = models.IntegerField(verbose_name='单词ID')
    question = models.CharField(max_length=500, verbose_name='题目')
    correct_answer = models.CharField(max_length=500, verbose_name='正确答案')
    user_answer = models.CharField(max_length=500, blank=True, default='', verbose_name='用户答案')
    is_correct = models.BooleanField(default=False, verbose_name='是否正确')

    class Meta:
        db_table = 'quiz_detail'

    def __str__(self):
        return f'{self.question} - {"✓" if self.is_correct else "✗"}'
