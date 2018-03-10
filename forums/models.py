from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.contrib.auth.models import User

##版块
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_topics', args=[self.pk])

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

##主题
class Topic(models.Model):
    ##帖子标题
    subject = models.CharField(max_length=256)
    last_updated = models.DateTimeField(auto_now_add=True)
    ##版块
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='topics',
    )
    ##帖子创建者
    starter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='topics',
    )
    ##浏览次数
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    ##获取绝对路径
    def get_absolute_url(self):
        return reverse('topic_posts', kwargs={
            'name': self.board.name,
            'topic_pk': self.pk
        })

##帖子内容
class Post(models.Model):
    #内容
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='+',
    )




    def __str__(self):
        truncated = Truncator(self.message)
        return truncated.chars(30)
