from django.db import models
from django.contrib.auth.models import User


class DailyProgress(models.Model):
    """每日学习进度"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_progress')
    date = models.DateField(verbose_name='日期')
    words_learned = models.IntegerField(default=0, verbose_name='学习单词数')
    words_reviewed = models.IntegerField(default=0, verbose_name='复习单词数')
    quiz_count = models.IntegerField(default=0, verbose_name='测验次数')
    study_minutes = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    checked_in = models.BooleanField(default=False, verbose_name='是否打卡')

    class Meta:
        db_table = 'daily_progress'
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.date}'
