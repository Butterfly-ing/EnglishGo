from django.db import models


class Article(models.Model):
    """英文文章"""
    LEVEL_CHOICES = [
        ('beginner', '入门'),
        ('intermediate', '中级'),
        ('advanced', '高级'),
    ]

    title = models.CharField(max_length=300, verbose_name='标题')
    title_cn = models.CharField(max_length=300, blank=True, default='', verbose_name='中文标题')
    author = models.CharField(max_length=100, blank=True, default='EnglishGo', verbose_name='作者')
    content = models.TextField(verbose_name='正文（英文）')
    content_cn = models.TextField(blank=True, default='', verbose_name='中文翻译')
    summary = models.TextField(blank=True, default='', verbose_name='摘要')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate', verbose_name='难度')
    tags = models.CharField(max_length=300, blank=True, default='', verbose_name='标签（逗号分隔）')
    word_count = models.IntegerField(default=0, verbose_name='字数')
    read_count = models.IntegerField(default=0, verbose_name='阅读次数')
    source_url = models.URLField(blank=True, default='', verbose_name='来源链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'article'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 自动计算字数
        self.word_count = len(self.content.split())
        super().save(*args, **kwargs)
