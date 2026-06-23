from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.username
