import re

from django.contrib.auth.models import User
from django.db import models


def get_default_user():
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(
            username="defaultuser", password="defaultpassword"
        )
    return user.id


class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE, default=get_default_user
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.title} by {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like on {self.post.title} by {self.created_at}"


class TrendingTopic(models.Model):
    topic = models.CharField(max_length=255, unique=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.topic


def update_trending_topics(content):
    topics = re.findall(r"#(\w+)", content)
    for topic in topics:
        trending_topic, created = TrendingTopic.objects.get_or_create(topic=topic)
        trending_topic.count += 1
        trending_topic.save()


def get_trending_topics():
    return TrendingTopic.objects.order_by("-count")[:10]
