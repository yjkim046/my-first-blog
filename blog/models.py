from django.db import models
from django.utils import timezone

class Nickname(models.Model):
    nid = models.IntegerField(default=1)
    name = models.CharField(max_length=200)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    thread_no = models.IntegerField(default=1)
    comment_cnt = models.IntegerField(default=0)
    num_user_comment = models.IntegerField(default=0)
    num_user_report = models.IntegerField(default=0)
    nickname = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    num_recommendation = models.IntegerField(default=0)
    num_read = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    within_post_id = models.IntegerField(default=1) 
    author = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
