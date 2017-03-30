from django.db import models
from django.utils import timezone

class Nickname(models.Model):
    nid = models.IntegerField(default=1)
    name = models.CharField(max_length=200)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    thread_no = models.IntegerField(default=1)
    comment_cnt = models.IntegerField(default=0)
    nickname = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    num_recommendation = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    within_post_id = models.IntegerField(default=1) 
    author = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
