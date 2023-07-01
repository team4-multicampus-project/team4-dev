from django.db import models
from account.models import CustomUser
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='')
    subject = models.CharField('제목', max_length=200)
    content = models.TextField('내용')
    created_at = models.DateTimeField('날짜')
    modify_date = models.DateTimeField(null=True, blank=True)
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    content = models.TextField('내용')
    created_at = models.DateTimeField('날짜')
    modify_date = models.DateTimeField(null=True, blank=True)